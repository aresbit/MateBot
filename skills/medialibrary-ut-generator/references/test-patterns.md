# Media Library UT Test Patterns

This document provides detailed test patterns derived from PR #10931 and other media library UT test files.

## Test Case Numbering Convention

Test cases follow a strict numbering pattern:
- Format: `<FeatureName>_test_<3-digit-number>`
- Examples: `SmartDataCleanState_test_001`, `AddAssets_Test_001`

Number ranges indicate test purpose:
- `_001` to `_020`: Basic functionality and happy path
- `_021` to `_040`: Error handling and negative cases
- `_041` to `_060`: Boundary conditions
- `_061` to `_080`: Integration tests
- `_081` to `_099`: Stress/performance tests

## Pattern 1: State Management Tests

From `cloud_media_retain_smart_data_test.cpp`:

### Single State Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataCleanState_test_001, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataCleanState_test_001 Start");
    SetSmartDataCleanState(CleanTaskState::CLEANING);
    int64_t state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::CLEANING));
    MEDIA_INFO_LOG("SmartDataCleanState_test_001 End");
}
```

### State Transition Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataCleanState_test_004, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataCleanState_test_004 Start");
    SetSmartDataCleanState(CleanTaskState::CLEANING);
    int64_t state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::CLEANING));
    SetSmartDataCleanState(CleanTaskState::IDLE);
    state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::IDLE));
    MEDIA_INFO_LOG("SmartDataCleanState_test_004 End");
}
```

### Default State Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataUpdateState_test_007, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataUpdateState_test_007 Start");
    int64_t state = GetSmartDataUpdateState();
    EXPECT_EQ(state, static_cast<int64_t>(UpdateSmartDataState::IDLE));
    MEDIA_INFO_LOG("SmartDataUpdateState_test_007 End");
}
```

## Pattern 2: Timestamp/Time Tests

### Time Setting Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataRetainTime_test_009, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataRetainTime_test_009 Start");
    SetSmartDataRetainTime();
    int64_t time = GetSmartDataRetainTime();
    EXPECT_GT(time, 0);
    MEDIA_INFO_LOG("SmartDataRetainTime_test_009 End");
}
```

### Time Comparison Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataRetainTime_test_011, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataRetainTime_test_011 Start");
    SetSmartDataRetainTime();
    int64_t time1 = GetSmartDataRetainTime();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    SetSmartDataRetainTime();
    int64_t time2 = GetSmartDataRetainTime();
    EXPECT_GT(time2, time1);
    MEDIA_INFO_LOG("SmartDataRetainTime_test_011 End");
}
```

## Pattern 3: Enum/Mode Tests

### Mode Setting Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataProcessingMode_test_013, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataProcessingMode_test_013 Start");
    SetSmartDataProcessingMode(SmartDataProcessingMode::NONE);
    SmartDataProcessingMode mode = GetSmartDataProcessingMode();
    EXPECT_EQ(mode, SmartDataProcessingMode::NONE);
    MEDIA_INFO_LOG("SmartDataProcessingMode_test_013 End");
}
```

### Conditional Check Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, IsNeedRecoverSmartData_test_018, TestSize.Level1)
{
    MEDIA_INFO_LOG("IsNeedRecoverSmartData_test_018 Start");
    SetSmartDataProcessingMode(SmartDataProcessingMode::RECOVER);
    bool needRecover = IsNeedRecoverSmartData();
    EXPECT_TRUE(needRecover);
    MEDIA_INFO_LOG("IsNeedRecoverSmartData_test_018 End");
}

HWTEST_F(CloudMediaRetainSmartDataTest, IsNeedRecoverSmartData_test_019, TestSize.Level1)
{
    MEDIA_INFO_LOG("IsNeedRecoverSmartData_test_019 Start");
    SetSmartDataProcessingMode(SmartDataProcessingMode::RETAIN);
    bool needRecover = IsNeedRecoverSmartData();
    EXPECT_FALSE(needRecover);
    SetSmartDataProcessingMode(SmartDataProcessingMode::NONE);
    needRecover = IsNeedRecoverSmartData();
    EXPECT_FALSE(needRecover);
    MEDIA_INFO_LOG("IsNeedRecoverSmartData_test_019 End");
}
```

## Pattern 4: Database Table Operation Tests

### Table Initialization Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, BackupPhotosAlbumTable_test_033, TestSize.Level1)
{
    MEDIA_INFO_LOG("BackupPhotosAlbumTable_test_033 Start");
    InitBackupPhotosAlbumTable();
    std::string checkSql = "SELECT count(*) FROM PhotosAlbumBackupForSaveAnalysisData";
    auto resultSet = g_rdbStore->QuerySql(checkSql);
    ASSERT_NE(resultSet, nullptr);
    int32_t rowCount = 0;
    resultSet->GetRowCount(rowCount);
    resultSet->Close();
    EXPECT_GE(rowCount, 0);
    MEDIA_INFO_LOG("BackupPhotosAlbumTable_test_033 End");
}
```

### Data Insert and Verify Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, BackupPhotosAlbumTable_test_035, TestSize.Level1)
{
    MEDIA_INFO_LOG("BackupPhotosAlbumTable_test_035 Start");
    InitBackupPhotosAlbumTable();
    int64_t albumId = 0;
    InsertAlbumForBackup(albumId);
    BackupBackupPhotosAlbumTable();
    std::string checkSql = "SELECT count(*) FROM PhotosAlbumBackupForSaveAnalysisData";
    auto resultSet = g_rdbStore->QuerySql(checkSql);
    ASSERT_NE(resultSet, nullptr);
    int32_t rowCount = 0;
    resultSet->GetRowCount(rowCount);
    resultSet->Close();
    EXPECT_GT(rowCount, 0);
    MEDIA_INFO_LOG("BackupPhotosAlbumTable_test_035 End");
}
```

### Update Operation Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, UpdateInvalidCloudHighlightInfo_test_040, TestSize.Level1)
{
    MEDIA_INFO_LOG("UpdateInvalidCloudHighlightInfo_test_040 Start");
    std::string insertSql = "INSERT INTO tab_highlight_album (highlight_status) VALUES (0)";
    g_rdbStore->ExecuteSql(insertSql);
    insertSql = "INSERT INTO tab_highlight_album (highlight_status) VALUES (1)";
    g_rdbStore->ExecuteSql(insertSql);
    insertSql = "INSERT INTO tab_highlight_album (highlight_status) VALUES (-3)";
    g_rdbStore->ExecuteSql(insertSql);
    UpdateInvalidCloudHighlightInfo();
    std::string checkSql = "SELECT highlight_status FROM tab_highlight_album WHERE highlight_status = -4";
    auto resultSet = g_rdbStore->QuerySql(checkSql);
    ASSERT_NE(resultSet, nullptr);
    int32_t rowCount = 0;
    resultSet->GetRowCount(rowCount);
    EXPECT_GT(rowCount, 0);
    resultSet->Close();
    MEDIA_INFO_LOG("UpdateInvalidCloudHighlightInfo_test_040 End");
}
```

## Pattern 5: Async Operation Tests

### Async Function Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, DoCleanPhotosTableCloudData_test_043, TestSize.Level1)
{
    MEDIA_INFO_LOG("DoCleanPhotosTableCloudData_test_043 Start");
    InitBackupPhotosAlbumTable();
    int32_t ret = DoCleanPhotosTableCloudData();
    EXPECT_EQ(ret, E_OK);
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    MEDIA_INFO_LOG("DoCleanPhotosTableCloudData_test_043 End");
}
```

## Pattern 6: Service API Tests

From `change_assets_test.cpp` and `album_add_assets_test.cpp`:

### Request/Response Marshalling Test
```cpp
HWTEST_F(AlbumAddAssetsTest, AddAssets_Test_001, TestSize.Level0)
{
    MEDIA_INFO_LOG("Start AddAssets_Test_001");
    // 1、前置条件准备，创建一个相册
    string albumName = "test01";
    CreateUserAlbum(albumName);

    // 2、查询相册id
    vector<string> columns;
    auto resultSet = QueryAsset(albumName, columns);
    ASSERT_NE(resultSet, nullptr);
    int32_t albumId = GetInt32Val(PhotoAlbumColumns::ALBUM_ID, resultSet);
    EXPECT_GT(albumId, 0);

    // 3、添加资产到用户相册
    vector<string> assetsArray = { "file://media/Photo/3/IMG_1748423717_002/IMG_20250528_171337.jpg" };
    int32_t changedRows = AddAssetsToAlbum(albumId, PhotoAlbumType::USER, PhotoAlbumSubType::USER_GENERIC, {});
    EXPECT_EQ(changedRows, E_INVALID_VALUES);

    changedRows = AddAssetsToAlbum(albumId, PhotoAlbumType::SYSTEM, PhotoAlbumSubType::USER_GENERIC, assetsArray);
    EXPECT_EQ(changedRows, E_INVALID_VALUES);

    changedRows = AddAssetsToAlbum(albumId, PhotoAlbumType::USER, PhotoAlbumSubType::SYSTEM_START, assetsArray);
    EXPECT_EQ(changedRows, E_INVALID_VALUES);

    changedRows = AddAssetsToAlbum(albumId, PhotoAlbumType::USER, PhotoAlbumSubType::USER_GENERIC, assetsArray);
    EXPECT_GT(changedRows, 0);
    MEDIA_INFO_LOG("end AddAssets_Test_001");
}
```

### Error Handling Test
```cpp
HWTEST_F(ChangeAssetsTest, AddAssets_Test_002, TestSize.Level0) {
    MessageParcel data;
    MessageParcel reply;

    auto service = make_shared<MediaAlbumsControllerService>();
    service->AddAssets(data, reply);

    IPC::MediaRespVo<AlbumPhotoQueryRespBody> respVo;
    ASSERT_EQ(respVo.Unmarshalling(reply), true);
    ASSERT_LT(respVo.GetErrCode(), 0);
}
```

## Pattern 7: Boundary Condition Tests

### Invalid Enum Value Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, BoundaryConditions_test_056, TestSize.Level1)
{
    MEDIA_INFO_LOG("BoundaryConditions_test_056 Start");
    CleanTaskState invalidState = static_cast<CleanTaskState>(999);
    SetSmartDataCleanState(invalidState);
    int64_t state = GetSmartDataCleanState();
    EXPECT_EQ(state, 999);
    MEDIA_INFO_LOG("BoundaryConditions_test_056 End");
}
```

### Empty Input Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, UpdatePhotosLcdVisitTime_test_051, TestSize.Level1)
{
    MEDIA_INFO_LOG("UpdatePhotosLcdVisitTime_test_051 Start");
    std::vector<std::string> fileIds;
    int32_t ret = UpdatePhotosLcdVisitTime(fileIds);
    EXPECT_EQ(ret, E_ERR);
    MEDIA_INFO_LOG("UpdatePhotosLcdVisitTime_test_051 End");
}
```

### Non-existent Data Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, UpdatePhotosLcdVisitTime_test_052, TestSize.Level1)
{
    MEDIA_INFO_LOG("UpdatePhotosLcdVisitTime_test_052 Start");
    std::vector<std::string> fileIds = {"999999", "999998"};
    int32_t ret = UpdatePhotosLcdVisitTime(fileIds);
    EXPECT_EQ(ret, E_ERR);
    MEDIA_INFO_LOG("UpdatePhotosLcdVisitTime_test_052 End");
}
```

## Pattern 8: Integration Tests

### Multi-Step Integration Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, IntegrationTest_test_064, TestSize.Level1)
{
    MEDIA_INFO_LOG("IntegrationTest_test_064 Start");
    InitBackupPhotosAlbumTable();
    SetSmartDataProcessingMode(SmartDataProcessingMode::RETAIN);
    SetSouthDeviceNextStatus(CloudMediaRetainType::RETAIN_FORCE, SwitchStatus::HDC);
    BackupBackupPhotosAlbumTable();
    SetSmartDataRetainTime();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    MEDIA_INFO_LOG("IntegrationTest_test_064 End");
}
```

### State Machine Integration Test
```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, IntegrationTest_test_066, TestSize.Level1)
{
    MEDIA_INFO_LOG("IntegrationTest_test_066 Start");
    SetSmartDataCleanState(CleanTaskState::IDLE);
    SetSmartDataCleanState(CleanTaskState::CLEANING);
    int64_t state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::CLEANING));
    SetSmartDataCleanState(CleanTaskState::IDLE);
    state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::IDLE));
    MEDIA_INFO_LOG("IntegrationTest_test_066 End");
}
```

## Test Comment Patterns

For documenting test purpose in Chinese:

```cpp
/**
 * @tc.name  : TestName
 * @tc.number: TestNumber
 * @tc.desc  : 测试描述（中文）
 */
HWTEST_F(ChangeAssetsTest, MoveAssetsTest_001, TestSize.Level0)
{
    // 测试当输入参数有效时,MoveAssets 函数应成功更新数据库。
}
```

Common description patterns:
- `测试<函数名>常规流程` - Test normal workflow
- `测试当<条件>时,<函数名>函数应<预期结果>` - Test conditional behavior
- `测试当读取请求体失败时,<函数名>函数应返回错误` - Test error handling
- `测试<函数名>的<功能>-<场景>` - Test specific feature with scenario
