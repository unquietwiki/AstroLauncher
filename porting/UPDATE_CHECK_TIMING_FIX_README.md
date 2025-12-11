# Update Check Timing Fix

This patch fixes the server update check frequency, changing it from every 30 seconds to every 30 minutes.

## Problem

The JoeJoeTV fork was checking for server updates every 30 seconds (tied to the heartbeat interval), which is excessive and causes:
- Unnecessary API/RSS calls
- Excessive log messages
- Potential rate limiting issues
- Unnecessary system load

## Solution

Implemented a separate timing mechanism for update checks that runs every 30 minutes (1800 seconds), matching the logic from the unquietwiki fork.

## Changes Made

### File: `cogs/AstroDedicatedServer.py`

#### 1. Added `lastUpdateCheck` Variable (Line 68)
```python
self.lastUpdateCheck = None
```

This new instance variable tracks when the last update check occurred, separate from the heartbeat timing.

#### 2. Moved Update Check Logic (Lines 399-409)
The update check logic was moved from inside the heartbeat check (30 seconds) to its own separate timing block (30 minutes).

**Before:**
```python
if self.lastHeartbeat is None or (now - self.lastHeartbeat).total_seconds() > 30:
    try:
        needs_update, latest_version = self.launcher.check_for_server_update(
            serverStart=True, check_only=True)
        # ... update logic ...
    except:
        pass
```

**After:**
```python
# Try to update every 30 minutes
if self.lastUpdateCheck is None or (now - self.lastUpdateCheck).total_seconds() > 1800:
    try:
        needs_update, latest_build = self.launcher.check_for_server_update(serverStart=True, check_only=True)
        if needs_update and self.launcher.launcherConfig.AutoUpdateServerSoftware:
            self.save_and_shutdown()
            self.launcher.update_server(latest_build)
            continue
    except Exception as e:
        AstroLogging.logPrint(f"Failed to check for server update: {e}", "debug")
    self.lastUpdateCheck = datetime.datetime.now()
```

#### 3. Improved Error Handling
- Changed bare `except:` to `except Exception as e:`
- Added debug logging for failed update checks
- Removed redundant log message

## Key Differences

| Aspect | Before (JoeJoeTV) | After (Fixed) |
|--------|-------------------|---------------|
| Check Frequency | Every 30 seconds | Every 30 minutes (1800 seconds) |
| Timing Variable | `lastHeartbeat` | `lastUpdateCheck` |
| Tied to Heartbeat | Yes | No (independent) |
| Error Handling | Silent (`except: pass`) | Logged (`except Exception as e:`) |

## Benefits

1. **Reduced Load**: 60x fewer update checks (from 120/hour to 2/hour)
2. **Better Logging**: Failed checks are now logged for debugging
3. **Rate Limit Friendly**: Reduces risk of hitting SteamDB RSS rate limits
4. **Separation of Concerns**: Update checks independent from heartbeat
5. **Cleaner Logs**: No spam about checking for updates

## Testing

To verify the fix is working:

1. **Check the logs** - You should see "Checking for AstroServer update" approximately every 30 minutes
2. **Monitor timing** - Note the timestamp of each check; they should be ~30 minutes apart
3. **Watch for errors** - Any update check failures will now be logged with details

Example log output:
```
[2025-12-10 17:00:00] [INFO] Checking for AstroServer update
[2025-12-10 17:30:00] [INFO] Checking for AstroServer update
[2025-12-10 18:00:00] [INFO] Checking for AstroServer update
```

## Configuration

The 30-minute interval is hardcoded (1800 seconds). If you want to customize this:

Edit `cogs/AstroDedicatedServer.py` line 400:
```python
# Change 1800 to your desired interval in seconds
if self.lastUpdateCheck is None or (now - self.lastUpdateCheck).total_seconds() > 1800:
```

Common intervals:
- 15 minutes: `900`
- 30 minutes: `1800` (default)
- 1 hour: `3600`
- 2 hours: `7200`

## Application

Apply the patch:
```bash
cd AstroLauncher_JoeJoeTV
git apply porting/UPDATE_CHECK_TIMING_FIX.patch
```

Or manually apply the changes as described above.

## Compatibility

- Compatible with existing launcher configurations
- No changes to user settings required
- Works with both automatic and manual update modes
- Compatible with DetermineServerBuild module

## Rollback

To revert:
```bash
git revert <commit-hash>
```

Or manually:
1. Remove `self.lastUpdateCheck = None` from line 68
2. Move the update check logic back inside the heartbeat check
3. Change `except Exception as e:` back to `except: pass`

## Related Changes

This fix complements:
- **DetermineServerBuild Port** - The update detection mechanism
- **Python 3.13 Migration** - Error handling improvements

## Version History

- **2025-12-10**: Initial fix - Changed from 30-second to 30-minute update checks

## Author

Ported from unquietwiki fork by Michael Adams with AI assistance
