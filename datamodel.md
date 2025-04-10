# Cricbuzz API Data Models

This document provides the data models for all the API responses from the Cricbuzz API.

## Venue Models

### Venue Stats

```typescript
interface VenueStats {
  venueStats: Array<{
    key: string;
    value: string;
  }>;
}
```

### Venue Matches

```typescript
interface VenueMatches {
  matchDetails: Array<{
    matchDetailsMap: {
      key: string;
      seriesId: number;
    };
  }>;
}
```

### Venue Details

```typescript
interface VenueDetails {
  ground: string;
  city: string;
  country: string;
  timezone: string;
  established: number;
  capacity: string;
  knownAs: string;
  ends: string;
  homeTeam: string;
  floodlights: boolean;
  profile: string;
  imageUrl: string;
  imageId: string;
}
```

## Player Models

### Player Bowling Stats

```typescript
interface PlayerBowlingStats {
  headers: string[];
  values: Array<{
    values: string[];
  }>;
  seriesSpinner: Array<{
    seriesName: string;
    seriesId?: number;
  }>;
}
```

### Player Batting Stats

```typescript
interface PlayerBattingStats {
  headers: string[];
  values: Array<{
    values: string[];
  }>;
  seriesSpinner: Array<{
    seriesName: string;
    seriesId?: number;
  }>;
}
```

### Player Details

```typescript
interface PlayerDetails {
  id: string;
  bat: string;
  bowl: string;
  name: string;
  nickName: string;
  role: string;
  birthPlace: string;
  intlTeam: string;
  teams: string;
  DoB: string;
  image: string;
  bio: string;
  rankings: {
    bat: {
      odiRank?: string;
      t20Rank?: string;
      testBestRank?: string;
      odiBestRank?: string;
      t20BestRank?: string;
      t20DiffRank?: string;
      odiDiffRank?: string;
    };
    bowl: {
      odiRank?: string;
      t20Rank?: string;
      testBestRank?: string;
      odiBestRank?: string;
      t20BestRank?: string;
      t20DiffRank?: string;
      odiDiffRank?: string;
    };
    all: {
      odiRank?: string;
      t20Rank?: string;
      odiBestRank?: string;
      t20BestRank?: string;
      t20DiffRank?: string;
      odiDiffRank?: string;
    };
  };
  DoBFormat: string;
  faceImageId: number;
  teamNameIds: Array<{
    teamId: string;
    teamName: string;
  }>;
  playerTeamIds: string;
}
```

### Player Search

```typescript
interface PlayerSearch {
  player: Array<{
    id: string;
    dob: string;
  }>;
  category: string;
}
```

### Trending Players

```typescript
interface TrendingPlayers {
  player: Array<{
    id: string;
    faceImageId: number;
  }>;
  category: string;
}
```

## Archives Models

### Archives Response (Common for all archive types)

```typescript
interface ArchivesResponse {
  seriesMapProto: Array<{
    date: string;
    series: Array<any>; // This can be expanded based on specific response
  }>;
}
```

## Schedules Models

### Schedules Response (Common for all schedule types)

```typescript
interface SchedulesResponse {
  matchScheduleMap: Array<{
    scheduleAdWrapper: {
      date: string;
      longDate: string;
    };
  }>;
}
```

## Team Models

### Team Stats

```typescript
interface TeamStats {
  filter: {
    matchtype: Array<{
      matchTypeId: string;
      matchTypeDesc: string;
    }>;
    team: Array<{
      id: string;
      teamShortName: string;
    }>;
    selectedMatchType: string;
    selectedTeam: string;
  };
  headers: string[];
  values: Array<{
    values: any[]; // Can be empty array or contain player stats
  }>;
  appIndex: {
    seoTitle: string;
    webURL: string;
  };
}
```

### Team Stats Types

```typescript
interface TeamStatsTypes {
  types: Array<{
    header?: string;
    value?: string;
    category?: string;
  }>;
  appIndex: {
    seoTitle: string;
    webURL: string;
  };
}
```

### Team Players

```typescript
interface TeamPlayers {
  player: Array<{
    name?: string;
    imageId?: number;
    id?: string;
    bowlingStyle?: string;
    battingStyle?: string;
  }>;
}
```

### Team News

```typescript
interface TeamNews {
  storyList: Array<{
    story: any; // Full story object structure
  }>;
  lastUpdatedTime: string;
  previousId: string;
}
```

### Team Results/Schedule

```typescript
interface TeamMatchesData {
  teamMatchesData: Array<{
    matchDetailsMap: any; // Match details object
  }>;
}
```

## Browse Team Models

### Browse Team Response (Common for all team types)

```typescript
interface BrowseTeamResponse {
  list: Array<{
    teamName?: string;
    teamId?: number;
    imageId?: number;
    countryName?: string;
    belongsTo?: string;
  }>;
  appIndex: {
    seoTitle: string;
    webURL: string;
  };
}
```

## Browse Series Models

### Browse Series Response (Common for all series types)

```typescript
interface BrowseSeriesResponse {
  seriesMapProto: Array<{
    date: string;
    series: Array<any>; // Series data
  }>;
  appIndex: {
    seoTitle: string;
    webURL: string;
  };
}
```

## Matches Models

### Matches Response (Common for recent, upcoming, live)

```typescript
interface MatchesResponse {
  typeMatches: Array<{
    matchType: string;
    seriesMatches?: Array<any>; // Array of series and their matches
  }>;
  filters: {
    matchType: string[];
  };
  appIndex?: {
    seoTitle: string;
    webURL: string;
  };
  responseLastUpdated: string;
}
```

## Series Models

### Series Points Table

```typescript
interface SeriesPointsTable {
  pointsTable: Array<{
    groupName: string;
    pointsTableInfo?: Array<any>; // Team standings information
  }>;
  appIndex: {
    seoTitle: string;
    webURL: string;
  };
}
```

### Series Venues

```typescript
interface SeriesVenues {
  seriesVenue: Array<{
    id: number;
    imageId: string;
  }>;
  seriesId: number;
  seriesName: string;
}
```

### Series Stats

```typescript
interface SeriesStats {
  odiStatsList?: {
    headers: string[];
    values: Array<any>;
  };
  t20StatsList?: {
    headers: string[];
    values: Array<any>;
  };
  filter: {
    matchtype: Array<any>;
  };
}
```

### Series Stats Types

```typescript
interface SeriesStatsTypes {
  types: Array<{
    header?: string;
    value?: string;
    category?: string;
  }>;
}
```

### Series Squad

```typescript
interface SeriesSquad {
  player: Array<{
    name?: string;
    isHeader?: boolean;
    id?: string;
    bowlingStyle?: string;
    battingStyle?: string;
  }>;
}
```

### Series Squads

```typescript
interface SeriesSquads {
  squads: Array<{
    squadType?: string;
    isHeader?: boolean;
    squadId?: number;
    teamId?: number;
  }>;
  appIndex: {
    seoTitle: string;
    webURL: string;
  };
  seriesName: string;
  seriesId: number;
}
```

### Series Details

```typescript
interface SeriesDetails {
  matchDetails: Array<{
    matchDetailsMap: any; // Match details
  }>;
}
```

## Match Models

### Match Highlights

```typescript
interface MatchHighlights {
  commentaryList: Array<{
    commText: string;
    commentaryFormats?: any;
  }>;
  matchHeader: {
    matchId: number;
    matchDescription: string;
    matchFormat: string;
    matchType: string;
    complete: boolean;
    domestic: boolean;
    matchStartTimestamp: number;
    matchCompleteTimestamp: number;
    dayNight: boolean;
    year: number;
    state: string;
    status: string;
    tossResults: {
      tossWinnerId: number;
      decision: string;
    };
    result: {
      resultType: string;
      winByInnings: boolean;
    };
    revisedTarget: {
      reason: string;
    };
    playersOfTheMatch: Array<any>;
    playersOfTheSeries: Array<any>;
    matchTeamInfo: Array<any>;
    isMatchNotCovered: boolean;
    team1: {
      id: number;
      shortName: string;
    };
    team2: {
      id: number;
      shortName: string;
    };
    seriesDesc: string;
    seriesId: number;
    seriesName: string;
    alertType: string;
    livestreamEnabled: boolean;
  };
  commentarySnippetList: Array<any>;
  page: string;
  enableNoContent: boolean;
  matchVideos: Array<any>;
  responseLastUpdated: number;
}
```

### Match Overs

```typescript
interface MatchOvers {
  inningsId: number;
  batsmanStriker: {
    batBalls: number;
    batDots: number;
    batFours: number;
    batId: number;
    batName: string;
    batMins: number;
    batRuns: number;
    batSixes: number;
    batStrikeRate: number;
  };
  batsmanNonStriker: {
    batBalls: number;
    batDots: number;
    batFours: number;
    batId: number;
    batName: string;
    batMins: number;
    batRuns: number;
    batSixes: number;
    batStrikeRate: number;
  };
  batTeam: {
    teamId: number;
    teamScore: number;
    teamWkts: number;
  };
  bowlerStriker: {
    bowlId: number;
    bowlName: string;
    bowlMaidens: number;
    bowlNoballs: number;
    bowlOvs: number;
    bowlRuns: number;
    bowlWides: number;
    bowlWkts: number;
    bowlEcon: number;
  };
  bowlerNonStriker: {
    bowlId: number;
    bowlName: string;
    bowlMaidens: number;
    bowlNoballs: number;
    bowlOvs: number;
    bowlRuns: number;
    bowlWides: number;
    bowlWkts: number;
    bowlEcon: number;
  };
  overs: number;
  recentOvsStats: string;
  target: number;
  partnerShip: {
    balls: number;
    runs: number;
  };
  currentRunRate: number;
  requiredRunRate: number;
  lastWicket: string;
  matchScoreDetails: {
    matchId: number;
    inningsScoreList: Array<any>;
    tossResults: {
      tossWinnerId: number;
      decision: string;
    };
    matchTeamInfo: Array<any>;
    isMatchNotCovered: boolean;
    matchFormat: string;
    state: string;
    customStatus: string;
    highlightedTeamId: number;
  };
  latestPerformance: Array<{
    runs: number;
    label: string;
  }>;
  ppData: {
    pp_1: {
      ppId: number;
      runsScored: number;
    };
  };
  matchUdrs: {
    matchId: number;
    inningsId: number;
    timestamp: string;
    team1Id: number;
    team1Remaining: number;
    team1Successful: number;
    team1Unsuccessful: number;
    team2Id: number;
    team2Remaining: number;
    team2Successful: number;
    team2Unsuccessful: number;
  };
  overSummaryList: Array<{
    score: number;
    event: string;
  }>;
  status: string;
  lastWicketScore: number;
  remRunsToWin: number;
  matchHeader: any; // Same as in MatchHighlights
  responseLastUpdated: number;
  event: string;
  overSepList: {
    overSummaryList: Array<any>;
    overSep: Array<any>;
  };
}
```

### Match Squads

```typescript
interface MatchSquads {
  team1: {
    team: {
      teamId: number;
      imageId: number;
    };
    players: {
      "playing XI": Array<any>;
    };
  };
  team2: {
    team: {
      teamId: number;
      imageId: number;
    };
    players: {
      "playing XI": Array<any>;
    };
  };
}
```

### Match Scorecard

```typescript
interface MatchScorecard {
  scoreCard: Array<any>; // Innings scorecard details
  matchHeader: any; // Same as in MatchHighlights
  isMatchComplete: boolean;
  status: string;
  videos: Array<any>;
  responseLastUpdated: number;
}
```

### Match Commentary

```typescript
interface MatchCommentary {
  commentaryList: Array<{
    commText: string;
    commentaryFormats?: any;
  }>;
  matchHeader: any; // Same as in MatchHighlights
  miniscore: {
    inningsId: number;
    batsmanStriker: {
      batBalls: number;
      batStrikeRate: number;
    };
    batsmanNonStriker: {
      batBalls: number;
      batStrikeRate: number;
    };
    batTeam: {
      teamId: number;
      teamWkts: number;
    };
    bowlerStriker: {
      bowlId: number;
      bowlEcon: number;
    };
    bowlerNonStriker: {
      bowlId: number;
      bowlEcon: number;
    };
    overs: number;
    recentOvsStats: string;
    target: number;
    partnerShip: {
      balls: number;
      runs: number;
    };
    currentRunRate: number;
    requiredRunRate: number;
    lastWicket: string;
    matchScoreDetails: {
      matchId: number;
      highlightedTeamId: number;
    };
    latestPerformance: Array<any>;
    ppData: {
      pp_1: any;
    };
    matchUdrs: {
      matchId: number;
      team2Unsuccessful: number;
    };
    overSummaryList: Array<any>;
    status: string;
    lastWicketScore: number;
    remRunsToWin: number;
    responseLastUpdated: number;
    event: string;
  };
  commentarySnippetList: Array<any>;
  page: string;
  enableNoContent: boolean;
  matchVideos: Array<any>;
  responseLastUpdated: number;
  cb11?: {
    team1Sname: string;
    team2Sname: string;
    title: string;
    imageId: number;
    appLink: string;
    webLink: string;
    isCb11Enabled: boolean;
  };
}
```

### Match Information

```typescript
interface MatchInfo {
  matchInfo: {
    matchId: number;
    matchDescription: string;
    matchFormat: string;
    matchType: string;
    complete: boolean;
    domestic: boolean;
    matchStartTimestamp: number;
    matchCompleteTimestamp: number;
    dayNight: boolean;
    year: number;
    state: string;
    team1: {
      id: number;
      shortName: string;
    };
    team2: {
      id: number;
      shortName: string;
    };
    series: {
      id: number;
      testSeriesResult: string;
    };
    umpire1: {
      id: number;
      country: string;
    };
    umpire2: {
      id: number;
      country: string;
    };
    umpire3: {
      id: number;
      country: string;
    };
    referee: {
      id: number;
      country: string;
    };
    tossResults: {
      tossWinnerId: number;
      decision: string;
    };
    result: {
      resultType: string;
      winByInnings: boolean;
    };
    venue: {
      id: number;
      longitude: string;
    };
    status: string;
    playersOfTheMatch: Array<any>;
    playersOfTheSeries: Array<any>;
    revisedTarget: {
      reason: string;
    };
    matchTeamInfo: Array<any>;
    isMatchNotCovered: boolean;
    HYSEnabled: number;
    livestreamEnabled: boolean;
    isFantasyEnabled: boolean;
    livestreamEnabledGeo: Array<any>;
    alertType: string;
    shortStatus: string;
    matchImageId: number;
  };
  venueInfo: {
    established: number;
    capacity: string;
    knownAs: string;
    ends: null;
    city: string;
    country: string;
    timezone: string;
    homeTeam: null;
    floodlights: boolean;
    curator: null;
    profile: null;
    imageUrl: string;
    ground: string;
    groundLength: number;
    groundWidth: number;
    otherSports: string;
  };
  broadcastInfo: Array<any>;
}
```
