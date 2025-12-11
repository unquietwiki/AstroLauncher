# DetermineServerBuild Port to JoeJoeTV Fork

This patch ports the `DetermineServerBuild` module from the unquietwiki fork to the JoeJoeTV fork of AstroLauncher.

## Overview

The `DetermineServerBuild` module provides a more reliable method for checking Astroneer dedicated server updates by:
- Parsing build version data from the SteamDB RSS feed
- Checking against the Steam `appmanifest_728470.acf` file
- Comparing build IDs instead of version strings

## Changes Made

### 1. New File: `cogs/DetermineServerBuild.py`
- Created new module with the following capabilities:
  - `getBuildsFromRSS()`: Fetches and parses build IDs from SteamDB RSS feed
  - `getBuildIDFromACF()`: Reads the current build ID from Steam's manifest file
  - `getCurrentBuildID()`: Returns the currently installed build ID
  - `getLatestBuildID()`: Returns the latest available build ID from RSS
  - `updateOK()`: Determines if an update is needed
  - `parse_manifest_kv()`: Parses Steam's ACF key-value format

### 2. Modified: `AstroLauncher.py`

#### Import Addition (Line 34)
```python
from cogs.DetermineServerBuild import DetermineServerBuild
```

#### Updated `check_for_server_update()` Method (Lines 530-575)
- **Removed**: API call to `https://astroservercheck.joejoetv.de/api/stats`
- **Removed**: Version string comparison using `version.parse()`
- **Added**: Integration with `DetermineServerBuild` module
- **Added**: Build ID comparison instead of version strings
- **Simplified**: Error handling and update logic flow
- **Fixed**: Proper return value when `UpdateOnServerRestart` is False

Key changes:
- Uses `DetermineServerBuild(self.astroPath)` to initialize version checker
- Calls `dbv.updateOK()` to determine if update is needed
- Uses `dbv.getCurrentBuildID()` and `dbv.getLatestBuildID()` for logging
- Passes build ID to `update_server()` instead of version string
- Reduced code complexity from ~70 lines to ~45 lines

## Benefits

1. **More Reliable**: Uses official Steam build IDs instead of third-party API
2. **Offline Capable**: Can determine current version from local files
3. **Better Error Handling**: Graceful degradation when RSS feed is unavailable
4. **Simpler Logic**: Cleaner code with fewer edge cases
5. **Independent**: No reliance on external server status APIs

## Dependencies

The module requires the `feedparser` library. Ensure it's included in your requirements:
```
feedparser
```

## Testing

To test the changes:
1. Apply the patch using `git apply DetermineServerBuild_port.patch`
2. Verify imports work: `python -c "from cogs.DetermineServerBuild import DetermineServerBuild"`
3. Run the launcher and check update detection
4. Monitor logs for "Checking for AstroServer update" message

## Compatibility Notes

- This change is backward compatible with existing launcher configurations
- The update mechanism remains the same; only the detection method changes
- Build IDs are passed to `update_server()` instead of version strings (should be compatible)

## Files Modified

- `cogs/DetermineServerBuild.py` (NEW)
- `AstroLauncher.py` (MODIFIED - import and check_for_server_update method)

## Application Instructions

From the JoeJoeTV fork root directory:
```bash
git apply DetermineServerBuild_port.patch
```

Or manually:
1. Copy `cogs/DetermineServerBuild.py` from unquietwiki fork
2. Add import in `AstroLauncher.py`
3. Replace `check_for_server_update()` method logic as shown in patch

## Author

Originally developed with AI assistance for the unquietwiki fork, ported to JoeJoeTV fork.
