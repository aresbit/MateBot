# OHOS App Build & Debug - Troubleshooting

Common issues and solutions when using the ohos-app-build-debug skill.

---

## DevEco Studio Not Detected

### Error Message
```
✗ 未检测到 DevEco Studio
```

### Solutions

1. **Verify Installation**
   - Confirm DevEco Studio is installed
   - Check standard locations:
     - Windows: `C:\Program Files\Huawei\DevEco Studio\`
     - macOS: `/Applications/DevEco-Studio.app/`
     - Linux: `~/DevEco-Studio/` or `/opt/DevEco-Studio/`

2. **Set Environment Variable**
   ```bash
   # macOS/Linux
   export DEVECO_STUDIO_PATH="/path/to/DevEco Studio"

   # Windows
   set DEVECO_STUDIO_PATH=C:\path\to\DevEco Studio
   ```

3. **Reinstall DevEco Studio**
   - Download from: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download
   - Ensure version 3.1+ (4.0+ recommended)

---

## SDK Components Not Found

### Error Message
```
✗ SDK components not found
```

### Solutions

1. **Open DevEco Studio**
   - Go to **Settings > SDK**
   - Install **HarmonyOS SDK** or **OpenHarmony SDK**
   - Ensure SDK is fully installed (not just downloaded)

2. **Check SDK Structure**
   ```
   DevEco Studio/sdk/
   ├── default/
   │   ├── openharmony/
   │   │   ├── toolchains/
   │   │   │   ├── hdc
   │   │   │   ├── hvigorw
   │   │   │   └── ...
   ```

3. **Refresh Detection Cache**
   ```bash
   python3 $SKILL_DIR/scripts/env_detector.py --refresh
   ```

---

## Device Not Connected

### Error Message
```
✗ 未检测到已连接的设备
```

### Solutions

1. **Check Physical Connection**
   - Verify USB cable is properly connected
   - Try a different USB port
   - Try a different USB cable

2. **Enable USB Debugging on Device**
   - Settings > About Phone > Tap "Build Number" 7 times
   - Settings > System & Updates > Developer Options > USB Debugging
   - Enable "USB Debugging" and "HDC Debugging"

3. **Authorize USB Debugging**
   - When prompted on device, tap "Allow" or "Trust"
   - Check "Always allow from this computer" if available

4. **macOS Specific**
   - Accept connection prompt when appears
   - Check System Preferences > Security & Privacy

5. **Verify Device Connection**
   ```bash
   # List connected devices
   hdc list targets

   # If hdc not found, ensure environment is detected
   python3 $SKILL_DIR/scripts/env_detector.py
   ```

---

## Build Failures

### Common Issues

#### 1. Module Not Found
**Error**: `Module not found: @ohos/xxx`

**Solution**:
```bash
# Install dependencies
ohpm install

# Or use DevEco Studio: Terminal > ohpm install
```

#### 2. Compilation Error
**Error**: `Failed to compile`

**Solution**:
- Check syntax errors in code
- Verify API level compatibility
- Check DevEco Studio build logs for details

#### 3. Signing Issues
**Error**: `Signature verification failed`

**Solution**:
- Ensure debug signature is configured
- Check `build-profile.json5` signing config
- Use DevEco Studio to auto-generate debug signature

#### 4. Out of Memory
**Error**: `java.lang.OutOfMemoryError`

**Solution**:
```bash
# Increase heap size in gradle.properties
org.gradle.jvmargs=-Xmx2048m
```

---

## Installation Failures

### Common Issues

#### 1. Signature Mismatch
**Error**: `INSTALL_FAILED_VERIFICATION_FAILURE`

**Solution**:
- Uninstall old version first:
  ```bash
   hdc shell bm uninstall -n com.example.app
  ```
- Use debug signature for testing

#### 2. Version Conflict
**Error**: `INSTALL_FAILED_UPDATE_INCOMPATIBLE`

**Solution**:
```bash
# Uninstall old version first
hdc shell bm uninstall -n com.example.app

# Then reinstall
python3 $SKILL_DIR/scripts/install.py -f app.hap
```

#### 3. Insufficient Storage
**Error**: `INSTALL_FAILED_INSUFFICIENT_STORAGE`

**Solution**:
- Free up device storage
- Install to external storage if available

#### 4. Permission Denied
**Error**: `INSTALL_FAILED_PERMISSION_DENIED`

**Solution**:
- Check app permissions in `module.json5`
- Ensure dangerous permissions are declared

---

## Launch Failures

### Common Issues

#### 1. App Not Installed
**Error**: `应用未安装`

**Solution**:
```bash
# Install the app first
python3 $SKILL_DIR/scripts/install.py -f app.hap

# Then launch
python3 $SKILL_DIR/scripts/launch.py
```

#### 2. Ability Not Found
**Error**: `Ability does not exist`

**Solution**:
- Verify ability name in `module.json5`
- Check default ability:
  ```bash
  python3 $SKILL_DIR/scripts/launch.py -a MainAbility
  ```

#### 3. API Level Mismatch
**Error**: `Device API level not supported`

**Solution**:
- Check device API level
- Update `compileSdkVersion` in `build-profile.json5`

---

## Script Execution Errors

### Python Not Found

**Error**: `python3: command not found`

**Solution**:
```bash
# Install Python 3.7+
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Windows
# Download from python.org
```

### Permission Denied

**Error**: `Permission denied: ./scripts/build.py`

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.py

# Or use python3 explicitly
python3 $SKILL_DIR/scripts/build.py
```

### Module Import Error

**Error**: `ImportError: No module named 'xxx'`

**Solution**:
- Ensure running from skill directory
- Check that `ohos_utils.py` is in `scripts/`
- Verify Python path includes scripts directory

---

## hdc Command Issues

### hdc Server Not Running

**Error**: `hdc server is not running`

**Solution**:
```bash
# Start hdc server
hdc start

# Kill and restart
hdc kill -r
hdc start
```

### Port Already in Use

**Error**: `Port 7035 already in use`

**Solution**:
```bash
# Kill existing hdc server
hdc kill

# Use different port
export HDC_SERVER_PORT=7036
```

---

## Getting Help

If issues persist:

1. **Check Detection Output**
   ```bash
   python3 $SKILL_DIR/scripts/env_detector.py --refresh
   ```

2. **Enable Verbose Logging**
   - Scripts show detailed command output
   - Check bash output for actual hvigorw/hdc commands

3. **DevEco Studio Logs**
   - View DevEco Studio build logs
   - Check `Help > Show Log in Finder/Explorer`

4. **Documentation**
   - HarmonyOS Docs: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/
   - OpenHarmony Docs: https://docs.openharmony.cn/
