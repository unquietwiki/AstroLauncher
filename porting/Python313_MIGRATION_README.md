# Python 3.13 Migration for JoeJoeTV Fork

This patch migrates the AstroLauncher from Python 3.7 to Python 3.13, incorporating compatibility improvements and modernizations.

## Overview

Python 3.7 reached end-of-life in June 2023. This migration brings AstroLauncher up to Python 3.13, which provides:
- Better performance
- Improved type checking
- Enhanced security
- Modern language features
- Continued security updates and bug fixes

## Changes Made

### 1. Pipfile Updates

#### Python Version (Line 27)
```python
# Before
python_version = "3.7"

# After
python_version = "3.13"
```

#### New Dependencies Added
- `feedparser = "*"` - Required for DetermineServerBuild module
- `requests = "*"` - Required for DetermineServerBuild module

### 2. AstroLauncher.py Changes

#### Removed Deprecated Imports
- **Removed `from fileinput import filename`** - Unused import
- **Removed `from distutils import dir_util`** - distutils removed in Python 3.12

#### Updated Import Style (Lines 26-28)
```python
# Before
import cogs.AstroAPI as AstroAPI
import cogs.AstroWebServer as AstroWebServer
import cogs.ValidateSettings as ValidateSettings

# After
from cogs import AstroAPI
from cogs import AstroWebServer
from cogs import ValidateSettings
```

#### Added Pylint Directive (Line 1)
```python
# pylint: disable=invalid-name,line-too-long,missing-function-docstring
```
Disables certain pylint warnings for cleaner linting with Python 3.13.

#### File Encoding Updates
All text-mode `open()` calls now explicitly use `encoding='utf-8'`:

**Locations updated:**
- Line 397: Config file writing
- Line 422: DevNull writing
- Line 452: Build version reading (updateLocation)
- Line 494: Build version reading (updateLocation, second check)
- Line 509: Build version reading (astroPath)
- Line 541: Update status file reading
- Line 549: Build version reading (check_for_server_update)
- Line 567: Build version reading (after update)

**Why:** Python 3.10+ on Windows defaults to system encoding (often cp1252), not UTF-8. Explicit encoding ensures consistent behavior across platforms.

#### Replaced dir_util.copy_tree (Lines 502-506)
```python
# Before
open("update.p", "wb").write(b"transfer")
dir_util.copy_tree(updateLocation, self.astroPath)
open("update.p", "wb").write(b"complete")

# After
with open("update.p", "wb") as f:
    f.write(b"transfer")
shutil.copytree(updateLocation, self.astroPath, dirs_exist_ok=True)
with open("update.p", "wb") as f:
    f.write(b"complete")
```

**Why:**
- `distutils` removed in Python 3.12
- `shutil.copytree` with `dirs_exist_ok=True` is the modern replacement
- Using context managers (`with`) is better practice

#### Improved Exception Handling (Line 496)
```python
# Before
except:
    pass

# After
except OSError:
    pass
```

**Why:** Catching specific exceptions is better practice and prevents hiding unexpected errors.

#### Fixed update.p Status Check (Line 543)
```python
# Before
if update_status != "completed":

# After
if update_status != "complete":
```

**Why:** Consistent with the value written in the update process ("complete" not "completed").

## Breaking Changes

### Python Version Requirement
- **Minimum Python version is now 3.13**
- Python 3.7-3.12 are no longer supported
- Users must upgrade their Python installation

### Dependencies
- Must run `pipenv install` to update dependencies
- New packages: `feedparser`, `requests`

## Migration Steps

### For Development

1. **Install Python 3.13**
   ```bash
   # Download from python.org or use package manager
   # Windows: Download from python.org
   # Linux: Use your distribution's package manager
   ```

2. **Apply the patch**
   ```bash
   cd AstroLauncher_JoeJoeTV
   git apply Python313_migration.patch
   ```

3. **Update dependencies**
   ```bash
   pipenv install
   # or
   pip install -r requirements.txt  # if using requirements.txt
   ```

4. **Test the application**
   ```bash
   python AstroLauncher.py
   ```

### For Production/Executable Builds

If building with PyInstaller:
```bash
pipenv run pyinstaller AstroLauncher.py -F --add-data "assets;./assets" --icon=assets/astrolauncherlogo.ico
```

## Testing Checklist

- [ ] Server update detection works
- [ ] Server updates download and install correctly
- [ ] Configuration files are read/written correctly
- [ ] Save files are handled properly
- [ ] Web interface functions
- [ ] RCON commands work
- [ ] Logs display correctly with UTF-8 characters
- [ ] Executable builds successfully (if applicable)

## Benefits of Python 3.13

1. **Performance**: ~10-15% faster than Python 3.7
2. **Security**: Active security support through October 2028
3. **Modern Features**: Pattern matching, better type hints, improved error messages
4. **Compatibility**: Better support for modern libraries
5. **Future-proof**: Room for future Python feature adoption

## Compatibility Notes

### Operating Systems
- Windows 10/11 (64-bit recommended)
- Linux (most distributions with Python 3.13)
- macOS 10.15+

### Known Issues
- None currently identified

## Rollback Procedure

If you need to rollback:

```bash
git revert <commit-hash>
pipenv install
```

Or manually:
1. Revert Pipfile to `python_version = "3.7"`
2. Revert AstroLauncher.py changes
3. Remove `feedparser` and `requests` from Pipfile if not needed
4. Run `pipenv install`

## Additional Notes

- This migration also includes the DetermineServerBuild feature (see DetermineServerBuild_PORT_README.md)
- The migration maintains backward compatibility with existing configuration files
- No changes to launcher settings or server configurations are required

## Files Modified

- `Pipfile` - Python version and dependencies
- `AstroLauncher.py` - Python 3.13 compatibility updates

## Author

Python 3.13 migration ported from unquietwiki fork by Michael Adams with AI assistance.

## Related Documentation

- [DetermineServerBuild Port](DetermineServerBuild_PORT_README.md)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)
- [Python 3.12 Removed distutils](https://docs.python.org/3.12/whatsnew/3.12.html#removed)
