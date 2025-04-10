import asyncio
import inspect
import os
from importlib import import_module
from time import sleep, time
from typing import Any, AsyncGenerator, Callable, Iterable, List, Optional, Tuple, Union

import cv2
import easyocr
import numpy as np
import PIL
import PIL.Image
import PIL.ImageGrab
from pandas import DataFrame
from pyautogui import linear
from pyscreeze import ImageNotFoundException

from activities.cv import MouseButton, Point
from activities.cv import click as click_
from activities.cv import click_drag_copy_text as click_drag_copy_text_
from activities.cv import copy_selected_text as copy_selected_text_
from activities.cv import find_text
from activities.cv import generate_table_chunks as generate_table_chunks_
from activities.cv import get_im_box, get_im_location, im_exists
from activities.cv import key_press as key_press_
from activities.cv import keyboard_shortcut as keyboard_shortcut_
from activities.cv import move
from activities.cv import read_table as read_table_
from activities.cv import scroll, wait_for_screen_to_change
from activities.cv import (
    wait_for_screen_to_stop_changing as wait_for_screen_to_stop_changing_,
)
from activities.cv import write
from models.base_models import JorieBaseModel
from models.exceptions import (
    ElementNotFoundException,
    ExpectedSceneException,
    NavigationFailedException,
    StitchingException,
    TextNotFoundException,
)
from utilities import validation
from utilities.image import Box, Offset
from utilities.image import screenshot as screenshot_
from utilities.image import stitch_scroll_area as stitch_scroll_area_
from utilities.logger import JorieLogger
from utilities.ocr import OCREngine, ocr_image, pad_image

_CONFIDENCE = 0.85


logger = JorieLogger()


class Element(JorieBaseModel):
    """Represents a single element on the screen."""

    name: str | None = None
    im_name: str | None = None
    required: bool = False
    bbox: Box | None = None
    confidence: float = _CONFIDENCE
    search_timeout: int = (
        30  # NOTE: Set to 30 seconds to match the default timeout in the `CV.get_im_location()` function - bbell 01/14/25
    )
    offset: Offset = Offset(x=0, y=0)
    alpha_mask: bool = False
    region: Box | None = None
    ocr_text: str | None = None
    ocr_engine: OCREngine = OCREngine.AZURE
    ocr_index: int = 0

    # NOTE: We want to call `self.exists` in short, 1 second intervals to ensure that
    #   `self._check_exists → CV.get_im_location` recaptures the scene multiple times
    #   within the timeout period specified in the `wait_for_element` function.
    EXISTS_CHECK_INTERVAL: int = 1

    def __init__(
        self,
        *,
        name: str | None = None,
        im_name: str | None = None,
        required: bool = False,
        bbox: Box | None = None,
        confidence: float = _CONFIDENCE,
        search_timeout: int = 30,  # NOTE: Set to 30 seconds to match the default timeout in the `CV.get_im_location()` function - bbell 01/14/25
        offset: Offset = Offset(x=0, y=0),
        alpha_mask: bool = False,
        region: Box | None = None,
        ocr_text: str | None = None,
        ocr_engine: OCREngine = OCREngine.AZURE,
        ocr_index: int = 0,
        text: str | None = None,
    ) -> None:
        """Initializes an Element object.

        Args:
            im_name (str, optional): The name of the image file representing the
                element. Defaults to None
            required (bool, optional): Whether the element is
                required to be present. Defaults to False.
            bbox (Box, optional): The bounding box of the element. Defaults to
                None.
            confidence (int, optional): The confidence level for locating the
                element. Defaults to 0.85.
            search_timeout (int, optional): The maximum time to search for the
                element on screen. Defaults to 30.
            offset (Offset, optional): Offset for performing clicks relative to
                the location of the element's centroid. Defaults to
                Offset(x=0, y=0).
            alpha_mask (bool, optional): Whether to use an alpha mast for image
                location. Defaults to False.
            region (Box, optional): The bounding box of the region in which to
                search for the element. Defaults to None.
            ocr_text (str, optional): The text to search for in the image.
                Defaults to None.
            ocr_engine (OCREngine, optional): The OCR engine to use. Defaults to
                OCREngine.AZURE.
            ocr_index (int, optional): The index of the OCR results to return.
                Defaults to 0.
        """
        super().__init__(
            name=name,
            im_name=im_name,
            required=required,
            bbox=bbox,
            confidence=confidence,
            search_timeout=search_timeout,
            offset=offset,
            alpha_mask=alpha_mask,
            region=region,
            ocr_text=ocr_text,
            ocr_engine=ocr_engine,
            ocr_index=ocr_index,
        )

        self_type_possibility_count: int = sum(
            [bool(im_name), bool(bbox), bool(ocr_text)]
        )
        if self_type_possibility_count == 0:
            raise ValueError(
                "Either `im_name`, `bbox`, or `ocr_text` must be provided."
            )
        elif self_type_possibility_count != 1:
            raise ValueError(
                "Exactly one of `im_name`, `bbox`, or `ocr_text` must be provided."
            )

        if self.name is None:
            self.name = (
                im_name
                if not all([bool(bbox), bool(ocr_text)])
                else (bbox if bool(bbox) else ocr_text)
            )

        if not any([self.im_name is None, self.region is None]):
            region_box: Box = Box(0, 0, self.region.width, self.region.height)
            im_box: Box = get_im_box(self.im_name)
            assert region_box.contains_box(im_box), ValueError(
                f"Element `{self.name}` has image dimensions exceeding its region dimensions. Im dim: `{im_box}`, Region dim: `{region_box}`"
            )

    @property
    def location(self) -> Optional[Point]:
        """Gets the location of the element.

        Raises:
            ElementNotFoundException: Raised when the Element is not found.

        Returns:
            Point: The location of the element.

        Raises:
            ElementNotFoundException
        """
        if self.ocr_text is not None:
            try:
                self.bbox = find_text(
                    self.ocr_text,
                    region=self.region,
                    engine=self.ocr_engine,
                    idx=self.ocr_index,
                )
                self._location = self.bbox.center
            except TextNotFoundException:
                raise ElementNotFoundException(
                    f"Element with text `{self.ocr_text}` not found using OCR."
                )
        elif self.bbox is not None:
            self._location = self.bbox.center
        else:
            try:
                # TODO: figure out timeout integration
                self._location = get_im_location(
                    self.im_name,
                    confidence=self.confidence,
                    timeout=self.search_timeout,
                    alpha_mask=self.alpha_mask,
                    region=(self.region.to_tuple() if self.region else None),
                )
            except ImageNotFoundException:
                raise ElementNotFoundException(
                    f"Element `{self.im_name}` not found after {self.search_timeout} seconds."
                )
        return self._location

    @property
    def bbox_on_screen(self) -> Optional[Box]:
        """Gets the bbox of the element (static if element if of bbox type, dynamic if of im or ocr_text types).

        Raises:
            ElementNotFoundException: Raised when the Element is not found.

        Returns:
            Box: The static or dynamic bbox of the element.

        Raises:
            ElementNotFoundException
        """
        if self.bbox is not None:
            self._bbox = self.bbox
        elif self.ocr_text is not None:
            try:
                self._bbox = find_text(
                    self.ocr_text,
                    region=self.region,
                    engine=self.ocr_engine,
                    idx=self.ocr_index,
                )
                self._bbox = (
                    Box(*self._bbox[0]) if isinstance(self._bbox, list) else self._bbox
                )
            except TextNotFoundException:
                raise ElementNotFoundException(
                    f"Element with text `{self.ocr_text}` not found using OCR."
                )
        else:
            try:
                # TODO: figure out timeout integration
                self._bbox = get_im_location(
                    self.im_name,
                    confidence=self.confidence,
                    timeout=self.search_timeout,
                    alpha_mask=self.alpha_mask,
                    region=(self.region.to_tuple() if self.region else None),
                    return_bbox=True,
                )
                self._bbox = Box(*self._bbox)
            except ImageNotFoundException:
                raise ElementNotFoundException(
                    f"Element `{self.im_name}` not found after {self.search_timeout} seconds."
                )

        if self.offset:
            self._bbox = self._bbox.shift(self.offset)

        return self._bbox

    @property
    def exists(self) -> bool:
        """Checks if an image exists on the screen.

        Returns:
            bool: True if the image is found, False otherwise.
        """
        # NOTE: We want to call `self._exists` with the default timeout specified in the `self.search_timeout` attribute
        return self.check_exists()

    def check_exists(self, timeout: int | None = None) -> bool:
        """
        Checks if an image exists on the screen with optional custom timeout.

        Args:
            timeout (int | None, optional): The maximum time to search for
                the element on screen. If None, defaults to self.search_timeout.

        Returns:
            bool: True if the element is found, False otherwise.
        """
        # Determine final timeout to use
        final_timeout = timeout if timeout is not None else self.search_timeout

        if timeout is not None:
            logger.debug(
                f"[exists] Overriding default search_timeout with caller-specified timeout: {final_timeout} seconds."
            )
        else:
            logger.debug(
                f"[exists] No caller-specified timeout. Using default search_timeout: {final_timeout} seconds."
            )

        # If this is an OCR-based element
        if self.ocr_text is not None:
            try:
                find_text(
                    self.ocr_text,
                    region=self.region,
                    engine=self.ocr_engine,
                    idx=self.ocr_index,
                )
                return True
            except TextNotFoundException:
                return False

        # If we have no pre-defined bbox, we look for the image
        elif self.bbox is None:
            return im_exists(
                self.im_name,
                confidence=self.confidence,
                timeout=final_timeout,
                region=(self.region.to_tuple() if self.region else None),
                alpha_mask=self.alpha_mask,
            )

        # If there's a static bbox, we consider it as existing by definition
        else:
            return True

    def wait_for_element(self, timeout: int = 30) -> None:
        """Waits for an element to appear on the screen.

        Args:
            timeout (int, optional): The maximum time to wait for the element to
                appear. Defaults to 30.

        Raises:
            ElementNotFoundException: Raised when the element does not appear
                before the timeout.
        """

        start_time = time()

        while time() - start_time < timeout:
            # NOTE: Call the internal `_exists` method to allow for custom timeout
            logger.debug("Waiting for element to appear...")
            if self.check_exists(self.EXISTS_CHECK_INTERVAL):
                return
        raise ElementNotFoundException(
            f"Element `{(self.im_name if self.im_name else self.ocr_text)}` not found after {timeout} seconds."
        )

    def click(
        self,
        *,
        clicks: int = 1,
        click_interval: float = 0.1,
        button: MouseButton | str = MouseButton.LEFT,
        pre_delay: float = 0.1,
        post_delay: float = 0.1,
        mouse_to_target_time: float = 0,
        mouse_to_target_tween: Callable[[Any], float] = linear,
    ) -> None:
        """Clicks at the point element.

        Args:
            clicks (int): number of clicks. Defaults to 1.
            click_interval (float): (seconds) click interval. Defaults to 0.5.
            button (MouseButton): LEFT or RIGHT or MIDDLE click. Defaults to
                MouseButton.LEFT.
            pre_delay (float, optional): _description_. Defaults to 0.1.
            post_delay (float, optional): _description_. Defaults to 0.1.
            mouse_to_target_time (float): (seconds) time to move mouse cursor to
                the element. Defaults to 0.
            mouse_to_target_tween: tween function: specifying velocity
                function/method/callable to move mouse cursor to the target point.
                Defaults to linear.

        Raises:
            AttributeError: for invalid input.
        """
        click_(
            self.location,
            offset=self.offset.to_tuple(),
            clicks=clicks,
            click_interval=click_interval,
            button=button,
            pre_delay=pre_delay,
            post_delay=post_delay,
            mouse_to_target_time=mouse_to_target_time,
            mouse_to_target_tween=mouse_to_target_tween,
        )

    def move_to(
        self,
    ) -> None:
        """Moves the mouse cursor to a specified location on the screen.

        Returns:
            None
        """
        move(self.location)

    def scroll_to(
        self,
        *,
        timeout: int = 30,
        method: str = "wheel",
        scroll_direction: str = "down",
        wheel_speed: int = 10,
        do_click: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        """Scrolls element into view.

        Args:
            im_name (str): Image name.
            timeout (int, optional): Time to perform scrolling. Defaults to 30.
            method (str, optional): Scrolling method; either "wheel" or
                "page_keys". Defaults to "wheel".
            scroll_direction (str, optional): Scroll direction; either "down" or
                "up". Defaults to "down".
            wheel_speed (int, optional): Rate at which scrolling is performed.
                Defaults to 10.
            do_click (bool, optional): Performs click when element is found.
                Defaults to False.

        Raises:
            ElementNotFound: Raised when element was not located before timeout
                was exceeded.
        """
        start_time = time()
        while time() - start_time < timeout:

            if self.exists:
                if do_click:
                    self.click(self.location, **kwargs)
                return
            else:
                if scroll_direction == "down":
                    if method == "wheel":
                        scroll(-abs(wheel_speed))  # TODO: use cv.scroll
                    elif method == "page_keys":
                        key_press_("page_down")
                elif scroll_direction == "up":
                    if method == "wheel":
                        scroll(wheel_speed)
                    elif method == "page_keys":
                        key_press_("page_up")
        else:
            raise ElementNotFoundException(
                f"Element `{(self.im_name if self.im_name else self.ocr_text)} not found after scrolling for {timeout} seconds."
            )

    def write_into(
        self, message: str, /, *, use_paste: bool = True, interval: float = 0.0
    ) -> None:
        """Writes a message into the element.

        Args:
            message (str): The message to write.
            use_paste (bool, optional): Use clipboard and paste to write if
                True. Defaults to True.
            interval (float, optional): The number of seconds in between each
                press. Defaults to 0.0.

        Returns:
            None
        """
        click_(self.location, offset=self.offset.to_tuple())
        write(message, use_paste=use_paste, interval=interval)

    def copy_text(
        self,
        *,
        clicks: int = 1,
        select_all: bool = True,
        post_click_delay: float = 0.25,
        clipboard_delay: float = 0.5,
    ):
        """Copies the selected text to the clipboard and returns it.

        This function simulates the keyboard shortcut for copying (Ctrl+C),
        waits for a short period to ensure the text is copied, then retrieves
        and returns the copied text from the clipboard.

        Args:
            clicks (int): Number of times to click element. Defaults to 1.
            select_all (str): Whether to send Ctrl+A. Defaults to True.
            post_click_delay (float): Number of seconds between click and copy
            clipboard_delay (float): Number of seconds between ctrl+c and getting the paste results.

        Returns:
            str: The text that was copied to the clipboard.
        """
        click_(self.location, offset=self.offset.to_tuple(), clicks=clicks)
        if select_all:
            keyboard_shortcut_("ctrl", "a")
        if post_click_delay:
            sleep(post_click_delay)
        return copy_selected_text_(delay=clipboard_delay)

    def ocr(self, image_np: np.ndarray, engine=OCREngine.EASYOCR) -> str:
        """Performs OCR on the given image using EasyOCR.

        Args:
            image (np.ndarray): The image to perform OCR on.

        Returns:
            str: The extracted text from the image.
        """
        if engine == OCREngine.EASYOCR:
            im = pad_image(image_np)
            im_arr = np.array(im)
            reader = easyocr.Reader(["en"])  # Initialize the OCREngine reader
            results = reader.readtext(im_arr)  # Perform OCR

            # Extract and concatenate the text from the results
            extracted_text = " ".join([text for (_, text, _) in results])

            return extracted_text
        elif engine == OCREngine.AZURE:
            return ocr_image(image_np)

    def get_ocr_text_from_element(self, engine=OCREngine.EASYOCR) -> str:
        """Gets the OCRed text of the element."""
        # Capture the screenshot of the bounding box
        if self.bbox is None:
            self.bbox = self.bbox_on_screen
        image = PIL.ImageGrab.grab(
            bbox=(
                self.bbox.left,
                self.bbox.top,
                self.bbox.left + self.bbox.width,
                self.bbox.top + self.bbox.height,
            )
        )

        # Convert the PIL Image to a NumPy array
        image_np = np.array(image)

        # Perform OCR on the clipped image
        return self.ocr(image_np, engine=engine)

    @property
    def text(self):
        """Gets the text of the element."""
        return self._text

    @text.setter
    def text(self, value):
        """Sets the text of the element."""
        self._text = value

    def read_table(
        self,
        *,
        scroll_speed: int = 10,
        key: str = None,
        presses: int = 1,
        move_to: Point = None,
        do_click: bool = False,
        scroll_delay: int = 1,
        iter_delay: int = 1,
        headers: list[str] = None,
        header_confidence: int = 0.8,
        local_ocr: bool = True,
        outlier_allowance_multiplier: float = 1.0,
        stack_images: bool = False,
        end_of_table: Callable[[Any | None], bool] | None = None,
        suppress_scrolling: bool = False,
    ) -> DataFrame:
        """OCRs scrollable table.

        Args:
            scroll_speed (int, optional): Speed at which to scroll using wheel.
                Defaults to 10.
            key (_type_, optional): Key to press; supports "down" and
                "page_down". Defaults to None.
            presses (int, optional): Number of key presses to perform. Defaults
                to 1.
            move_to (Point, optional): Position to move mouse to
                during capture. Defaults to None.
            do_click (bool, optional): Whether to perform a click at the
                supplied `move_to`. Defaults to False.
            delay (int, optional): Time to wait in seconds for after scrolling.
                Defaults to 1.
            headers (List[str]): List of header images.
            header_confidence (int, optional): Confidence threshold for locating
                headers. Defaults to 0.8.
            local_ocr (bool, optional): Whether to perform OCR locally; if
                false, throttled requests to Azure AI Vision will be used. Defaults
                to True.
            outlier_allowance_multiplier (float): Standard deviation multiplier
                to adjust allowance when filtering bad rows.
            stack_images (bool, optional): Whether to vertically stack the images.
                Defaults to False.

        Returns:
            DataFrame: DataFrame of OCR results.
        """
        return read_table_(
            self.bbox.to_tuple(),
            scroll_speed=scroll_speed,
            key=key,
            presses=presses,
            move_to=move_to.to_tuple() if move_to else None,
            do_click=do_click,
            scroll_delay=scroll_delay,
            iter_delay=iter_delay,
            headers=headers,
            header_confidence=header_confidence,
            local_ocr=local_ocr,
            outlier_allowance_multiplier=outlier_allowance_multiplier,
            stack_images=stack_images,
            end_of_table=end_of_table,
            suppress_scrolling=suppress_scrolling,
        )

    async def generate_table_chunks(
        self,
        *,
        scroll_speed: int = 10,
        key: str = None,
        presses: int = 1,
        move_to: Point = None,
        do_click: bool = False,
        scroll_delay: int = 1,
        iter_delay: int = 1,
        headers: list[str] = None,
        header_confidence: int = 0.8,
        local_ocr: bool = True,
        outlier_allowance_multiplier: float = 1.0,
        # stack_images=False, #  Only stacking is currently supported.
    ) -> AsyncGenerator[DataFrame, None]:
        """OCRs scrollable table.

        Args:
            scroll_speed (int, optional): Speed at which to scroll using wheel.
                Defaults to 10.
            key (_type_, optional): Key to press; supports "down" and
                "page_down". Defaults to None.
            presses (int, optional): Number of key presses to perform. Defaults
                to 1.
            move_to (Point, optional): Position to move mouse to
                during capture. Defaults to None.
            do_click (bool, optional): Whether to perform a click at the
                supplied `move_to`. Defaults to False.
            delay (int, optional): Time to wait in seconds for after scrolling.
                Defaults to 1.
            headers (List[str]): List of header images.
            header_confidence (int, optional): Confidence threshold for locating
                headers. Defaults to 0.8.
            local_ocr (bool, optional): Whether to perform OCR locally; if
                false, throttled requests to Azure AI Vision will be used. Defaults
                to True.
            outlier_allowance_multiplier (float): Standard deviation multiplier
                to adjust allowance when filtering bad rows.
            stack_images (bool, optional): Whether to vertically stack the images.
                Defaults to False.

        Returns:
            DataFrame: DataFrame of OCR results.
        """
        async for chunk in generate_table_chunks_(
            self.bbox.to_tuple(),
            scroll_speed=scroll_speed,
            key=key,
            presses=presses,
            move_to=move_to.to_tuple() if move_to else None,
            do_click=do_click,
            scroll_delay=scroll_delay,
            iter_delay=iter_delay,
            headers=headers,
            header_confidence=header_confidence,
            local_ocr=local_ocr,
            outlier_allowance_multiplier=outlier_allowance_multiplier,
            # stack_images=False, #  Only stacking is currently supported.
        ):
            yield chunk

    def wait_for_disappearance(
        self,
        *,
        timeout: int = 30,
        wait_for: int = 1,
    ) -> None:
        """Waits for an image to disappear from the screen.

        Args:
            confidence (float, optional): The confidence level for the image
                search. Defaults to 0.7. timeout (int, optional): The maximum
                time in seconds to wait for the image to disappear.. Defaults to
                30.
            wait_for (int, optional): The duration in seconds between calls to
            `im_exists`.. Defaults to 1.

        Raises:
            TimeoutError: If the image is still present after the timeout
            period.
        """
        start_time = time()
        while time() - start_time < timeout:
            if not self.exists():
                return
            sleep(wait_for)
        raise TimeoutError(
            f"Element {(self.im_name if self.im_name else self.ocr_text)} did not disappear within {timeout} seconds."
        )

    def ocr_scrollable(
        self,
        *,
        scroll_speed: int = 10,
        key: str | None = None,
        presses: int | None = None,
        move_to: Point | None = None,
        do_click: bool = False,
        scroll_delay: int = 1,
    ):
        try:
            im = stitch_scroll_area_(
                scroll,
                region=self.bbox,
                scroll_speed=scroll_speed,
                key=key,
                presses=presses,
                move_to=move_to,
                do_click=do_click,
                scroll_delay=scroll_delay,
            )
        except StitchingException:
            logger.warning(
                "Stitching failed. This is likely because the scrollable element did not change after scrolling. The image returned may not contain all the expected data."
            )
            im = screenshot_(region=self.bbox)
        return ocr_image(im)

    @classmethod
    def set_region_for_multiple_elements(
        cls, elements: Union["Element", Iterable["Element"]], region: Box
    ) -> None:
        """Sets the `region` attribute for multiple `Element` instances.

        Args:
            elements (Union[Element, Iterable[Element]]): `Element` instance or collection of `Element` instances for which region is to be set.
            region (Box): Incoming region bounding box to set.
        """
        arg_type = validation.assert_var_value_type(
            "elements", elements, (Element, Iterable)
        )
        if arg_type == Element:
            elements: list[Element] = [elements]
        else:
            assert all(
                [isinstance(element, Element) for element in elements]
            ), ValueError(
                f"All target elements should be Element type; provided types: {[str(type(element)) for element in elements]}."
            )

        for element in elements:
            element.region = region


class Scene:
    """A class used to represent a Scene.

    A Scene is a collection of Elements that are expected to be present together
    on the screen.

    Attributes:
        elements: An object containing the Elements in the Scene.
    """

    def __init__(self, elements):
        """
        Initializes a Scene with a set of Elements.

        Args:
            elements: An object containing the Elements in the Scene.
        """
        # assert isinstance(elements, type), ValueError("Must pass Locator class, not instance to Scene constructor") # TODO: confirm if this should be here
        self.elements = elements
        # assert any([element.required for element in self.elements.__dict__.values() if isinstance(element, Element)]), ValueError(f"Scene '{self.elements}' must have at least one 'required' element.") # TODO: custom exception

    def __repr__(self):
        return self.name

    @property
    def name(self) -> str:
        return self.elements.__name__

    def locate_required_elements(self):
        """Locates all required Elements in the Scene.

        For each Element in the Scene, if the Element is marked as required,
        this method attempts to locate the Element on the screen and stores its
        location.

        Raises:
            ElementNotFound: If a required Element cannot be located on the
                screen.
        """
        for element_name, element in self.elements.__dict__.items():
            if isinstance(element, Element):
                setattr(self, element_name, element)
                if element.required:
                    element._location = element.location

    def key_press(self, key: str, duration: float = 0.25):
        """Simulates a key press on the keyboard.

        This function presses a key, waits for a specified duration, and then
        releases the key. If the key string is longer than one character, it is
        mapped to the corresponding Key object. For example, pressing "a" is
        done by passing only the character, pressing "alt" is done by mapping to
        Key.alt and passing that object.

        Args:
            key (str): The key to press. Can be a single character or the name
            of a special key (e.g., "alt"). duration (float, optional): The
            duration to hold the key down in seconds. Defaults to 0.25.

        Returns:
            None
        """
        key_press_(key, duration=duration)

    def keyboard_shortcut(
        self,
        *keys: str,
        interval: float = 0.25,
        delay_after: float = 0.0,
    ):
        """Simulates a keyboard shortcut.

        This function simulates pressing a sequence of keys on the keyboard. Each key is pressed in the order they are given, held for a specified interval, and then released in reverse order.

        Args:
            *keys (str): The keys to press. Can be single characters or names of special keys (e.g., "alt").
            interval (float, optional): The duration to hold each key down in seconds. Defaults to 0.25.
            delay_after (float, optional): The delay after releasing the keys in seconds. Defaults to 0.0.

        Returns:
            None
        """
        keyboard_shortcut_(*keys, interval=interval, delay_after=delay_after)

    def wait_for_scene_to_stop_changing(
        self,
        increment: int = 0,
        wait_for: int = 2,
        timeout: int = 30,
        pixel_threshold: int = 40,
        region: tuple[int, int, int, int] | Box | None = None,
        ignore_region: tuple[int, int, int, int] | Box | None = None,
    ) -> None:
        """Waits until the screen stops changing for a specified amount of time or until the timeout is reached.

        Args:
            increment (int, optional): The interval in seconds between each screenshot. Defaults to 0.
            wait_for (int, optional): The duration in seconds to wait for the screen to stop changing. Defaults to 5.
            timeout (int, optional): The maximum time in seconds to wait before exiting the function. Defaults to 30.
            pixel_threshold (int, optional): The amount of pixels that are allowed to not stay the same. Default accounts for standard blinking caret/cursor. Defaults to 40.
            region (tuple[int, int, int, int] | Box | None, optional): Region of the screen to take the screenshot
            ignore_region (tuple[int, int, int, int] | Box | None, optional): Region of the screen to ignore

        Raises:
            TimeoutError: If the screen does not change within the timeout period.
        """
        logger.info("Waiting for scene to stop changing.")
        wait_for_screen_to_stop_changing_(
            increment=increment,
            wait_for=wait_for,
            timeout=timeout,
            pixel_threshold=pixel_threshold,
            region=region,
            ignore_region=ignore_region,
        )

    def wait_for_scene_to_change(
        self,
        increment: int = 0,
        timeout: int = 30,
        pixel_threshold: int = 0,
        region: tuple[int, int, int, int] | Box | None = None,
    ) -> None:
        """Waits until the screen starts changing or until the timeout is reached.

        Args:
            increment (int, optional): The interval in seconds between each
                screenshot. Defaults to 0.
            timeout (int, optional): The maximum time in seconds to wait before
                exiting the function. Defaults to 30.
            pixel_threshold (int, optional): The amount of pixels that are allowed
                to not stay the same.
            region (tuple[int, int, int, int] | Box | None, optional): Region of the
                screen to take the screenshot

        Raises:
            TimeoutError: If the screen does not change within the timeout period.
        """
        wait_for_screen_to_change(
            increment=increment,
            timeout=timeout,
            pixel_threshold=pixel_threshold,
            region=region,
        )

    def write(
        self, message: str, /, *, use_paste: bool = True, interval: float = 0.0
    ) -> None:
        """Writes a message.

        Args:
            message (str): The message to write.
            use_paste (bool, optional): Use clipboard and paste to write if
                True. Defaults to True.
            interval (float, optional): The number of seconds in between each
                press. Defaults to 0.0.

        Returns:
            None
        """
        write(message, use_paste=use_paste, interval=interval)

    def click_drag_copy_text(
        self,
        start: Point | tuple[int, int],
        end: Point | tuple[int, int],
        /,
        *,
        duration: float = 1,
        mouse_up_delay: float = 0,
    ) -> str:
        """Drags to select text and copy it to the clipboard.

        Args:
            start (Point | tuple[int, int]): Mouse down point.
            end (Point | tuple[int, int]): Mouse up point.
            duration (float, optional): Length of time from start to end points. Defaults to 1.
            mouse_up_delay (float, optional): The time between reaching the end point and
                lifting up off the mouse. Defaults to 0.

        Returns:
            str: Text copied to clipboard.
        """
        return click_drag_copy_text_(
            start, end, duration=duration, mouse_up_delay=mouse_up_delay
        )

    def copy_selected_text(self) -> str:
        """Copies the selected text and returns the string from the clipboard.

        Returns:
            str: Copied text.
        """
        return copy_selected_text_()


def screenshot(
    self, region: Box | None = None, return_pil_image: bool = False
) -> cv2.typing.MatLike | PIL.Image.Image:
    """Captures a screenshot and converts it to a format suitable for use with
    OpenCV.

    This function uses PIL's ImageGrab module to capture a screenshot. The
    screenshot is then converted to a NumPy array and its color format is
    converted from RGB (used by PIL) to BGR (used by OpenCV).

    Args:
        region (Box | None, optional): Region to crop screenshot to. Defaults to
            None.
        return_pil_image (bool, optional): Whether to return PIL Image object.
            Defaults to False.

    Returns:
        cv2.typing.MatLike | PIL.Image.Image: The screenshot as a NumPy array in
            BGRA format, or a PIL Image object in RGBA.
    """
    return screenshot_(region, return_pil_image=return_pil_image)


class SceneManager:
    """A class used to manage Scenes.

    A SceneManager is responsible for initializing the start scene and end scene
    (if provided), and ensuring that all required Elements in these scenes can
    be located.

    Attributes:
        start_scene (Scene): The starting Scene.
        end_scene (Scene, optional): The ending Scene. Defaults to None.
    """

    # @classmethod
    # def navigate_to(Scene):
    #     return

    # TODO: Decide whether end_scene should be a key word only arg
    def __init__(self, start_scene, end_scene=None):
        """Initializes a SceneManager with a start scene and an optional end scene.

        Args:
            start_scene (Scene): The starting Scene.
            end_scene (Scene, optional): The ending Scene. Defaults to None.
        """
        self.start_scene = Scene(start_scene)
        self.start_scene_name = start_scene.__name__

        if end_scene is not None:
            self.end_scene = Scene(end_scene)
            self.end_scene_name = end_scene.__name__
            logger.info(
                f"Navigating from `{self.start_scene_name}` to `{self.end_scene_name}`."
            )
        else:
            self.end_scene = None

    def __enter__(self):
        """Returns the start scene when entering the context.

        Returns:
            Scene: The starting Scene.
        """
        try:
            self.start_scene.locate_required_elements()
            # ^ TODO ensure that it distingished between Parent & Child scenes (to avoid False Positives)
            # ^ two alternatives:
            # 1. Use an instance of SceneDetector (pro: ready to use, con: potentially slower)
            # 2. Add parent-child relationship logic (maybe extract the logic from SceneDetector)
            logger.info(f"Found start scene `{self.start_scene_name}`.")
        except ElementNotFoundException as e:
            raise ExpectedSceneException(
                f"Expected scene `{self.start_scene_name}` not found.\n\n{str(e)}"
            )

        return self.start_scene

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Checks the end scene or the start scene when exiting the context.

        If an end scene is provided, it checks that all required Elements in the
        end scene can be located. If not, it raises a NavigationFailedException.
        If no end scene is provided, it checks that all required Elements in the
        start scene can still be located. If not, it raises an
        ExpectedSceneException.

        Args:
            exc_type: The type of exception raised within the context.
            exc_value: The instance of exception raised within the context.
            traceback: A traceback object encapsulating the call stack at the
                point where the exception was raised.

        Raises:
            NavigationFailedException: If the end scene is provided and any
                required Element in the end scene cannot be located.
            ExpectedSceneException: If no end scene is provided and any required
                Element in the start scene cannot be located.

        Returns:
            False
        """
        if exc_type:
            raise

        if self.end_scene:
            try:
                wait_for_screen_to_stop_changing_(
                    pixel_threshold=40
                )  # pixel threshold for blinking cursors/carets
                self.end_scene.locate_required_elements()
                logger.info(f"Found end scene `{self.end_scene_name}`.")
            except ElementNotFoundException as e:
                raise NavigationFailedException(
                    f"End scene `{self.end_scene_name}` not found.\n\n{str(e)}"
                )
        else:
            try:
                Scene(self.start_scene).locate_required_elements()
                logger.info(f"Found end scene `{self.start_scene_name}`.")
            except ElementNotFoundException as e:
                raise ExpectedSceneException(
                    f"Expected scene `{self.start_scene_name}` not found.\n\n{str(e)}"
                )
        return False


# TODO move to `utilities.scene`
def get_scenes() -> list[Scene]:
    """TODO: logic to retrieve list of Scenes from the scene locator file for a given client & project.
    - Refer to implementation of PopupHandler

    Returns:
        list[Scene]: _description_
    """
    dot_path = (
        f"scenes.{os.environ['CLIENT_NAME']}.{os.environ['PROCESS_NAME']}.locators"
    )
    module = import_module(dot_path)

    # Filter classes defined in the module
    return [
        Scene(obj)
        for _, obj in inspect.getmembers(module)
        if inspect.isclass(obj) and obj.__module__ == module.__name__
    ]


# TODO move to `utilities.scene`
class SceneDetector:
    self_ = None

    def __init__(self, scenes: list[Scene] = get_scenes()):
        self.scenes: list[Scene] = scenes

    async def detect(self) -> AsyncGenerator[Tuple[Scene, float], None]:
        """Detects which scenes the current scene could be. Yields scenes and confidences
        of scenes who have required elements on the current screen.

        Yields:
            Iterator[AsyncGenerator[Tuple[Scene, float], None]]: Yields tuples of scene and confidence
        """
        scene_confidence_map: dict[Scene, float] = {scene: 0 for scene in self.scenes}
        for scene in self.scenes:
            required_elements: list[Element] = self._get_required_elements(scene)

            # Check if required elements exist on screen
            tasks = [self._check_element(element) for element in required_elements]
            results = await asyncio.gather(*tasks)
            detected_required_elements_count: int = sum(results)

            if required_elements:
                # Populate confidence of the scene detected required element/ required elements
                scene_confidence_map[scene] = detected_required_elements_count / len(
                    required_elements
                )
        # Sort by confidence
        sorted_results = sorted(
            scene_confidence_map.items(), key=lambda item: item[1], reverse=True
        )

        for scene, confidence in sorted_results:
            if confidence == 1:
                yield scene, confidence

    def _get_required_elements(self, scene: Scene) -> List[Element]:
        """Extracts all require elements from a scene

        Args:
            scene (Scene): The scene to find required elements in

        Returns:
            List[Element]: The list of require elements
        """
        elements: dict[str, Element] = scene.elements.__dict__
        required_elements: list = []
        for element in elements.values():
            if not isinstance(element, Element):
                continue
            if element.required:
                required_elements.append(element)
        return required_elements

    async def _check_element(self, element: Element) -> int:
        """Searches for element on the current screen. Returns 1 if found.
        This is used to get a count of all required elements to determine confidence.

        Args:
            element (Element): The element to find.

        Returns:
            int: 1 if found, 0 otherwise
        """
        element.search_timeout = 1
        return 1 if element.exists else 0

    def orient(self) -> Scene:
        """Detects and returns the current scene.

        Returns:
            Scene: The current scene.
        """
        detected_scenes = [
            scene for scene, _ in asyncio.run(self._collect_detected_scenes())
        ]

        detected_scenes_err_str = ", ".join(
            [Scene(scene).elements.name for scene in detected_scenes]
        )

        if len(detected_scenes) == 1:
            return detected_scenes[0]
        elif len(detected_scenes) == 2:
            scene1, scene2 = detected_scenes
            if self._is_child_scene(child=scene1, parent=scene2):
                return scene1
            elif self._is_child_scene(child=scene2, parent=scene1):
                return scene2
            else:
                raise NotImplementedError(
                    f"Handling two unrelated elements is not implemented. Detected Scenes: {detected_scenes_err_str}."
                )
        else:
            raise NotImplementedError(
                f"Handling {len(detected_scenes)} detected scenes is not implemented. Detected Scenes: {detected_scenes_err_str}"
            )

    async def _collect_detected_scenes(self) -> List[Tuple[Scene, float]]:
        """Helper for orient to keep orient Synchronous"""
        detected_scenes = []
        async for scene, confidence in self.detect():
            detected_scenes.append((scene, confidence))
        return detected_scenes

    def _is_child_scene(self, child: Scene, parent: Scene) -> bool:
        """Detects whether the child scene is a child of the parent scene.

        Args:
            child (Scene): Scene to check if child of `parent` Scene.
            parent (Scene): Potential parent of `child` Scene

        Returns:
            bool: True if child, False if not
        """
        for attribute_name in dir(parent.elements):
            if not attribute_name.startswith("__"):
                attribute_value = getattr(parent.elements, attribute_name)
                if isinstance(attribute_value, Scene):
                    original_class_name = attribute_value.name
                    if original_class_name == child.name:
                        return True
        return False


understand 