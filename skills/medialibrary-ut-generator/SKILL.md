---
name: medialibrary-ut-generator
description: Generate unit tests (UT) for OpenHarmony multimedia media library C++ code. Use when creating new UT test files, modifying existing tests, or adding test cases for media library services, controllers, DAOs, and cloud sync components. Covers test patterns for MediaAssetsControllerService, MediaAlbumsControllerService, cloud media sync, background tasks, and database operations.
---

# OpenHarmony Media Library UT Generator

## Overview

This skill generates high-quality unit tests for OpenHarmony multimedia media library following project-specific patterns and best practices. It provides templates and patterns for testing services, controllers, DAOs, and cloud sync components.

## When to Use

Use this skill when:
- Creating new UT test files for media library components
- Adding test cases to existing test files
- Testing MediaAssetsControllerService or MediaAlbumsControllerService APIs
- Testing cloud media sync functionality
- Testing background task processors
- Testing database operations and DAOs

## Test File Structure

### Directory Layout
```
frameworks/innerkitsimpl/test/unittest/<test_name>/
├── BUILD.gn                    # Build configuration
├── include/
│   └── <test_name>_test.h      # Test class header
└── src/
    └── <test_name>_test.cpp    # Test implementation
```

### Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Test directory | `snake_case` | `cloud_media_retain_smart_data_test` |
| Test class | `PascalCase + Test` | `CloudMediaRetainSmartDataTest` |
| Test function | `HWTEST_F` with `TestSize.Level0/1` | `SmartDataCleanState_test_001` |
| Test case name | `snake_case + _test_ + number` | `add_assets_test_001` |

## Test Implementation Patterns

### 1. Standard Test Class Template

```cpp
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 */

#define MLOG_TAG "TestClassName"

#include "test_class_name_test.h"
#include <chrono>
#include <thread>
#include <vector>

// Access private/protected members for testing
#define private public
#define protected public
#include "target_class_header.h"
#undef private
#undef protected

#include "medialibrary_unittest_utils.h"
#include "medialibrary_unistore_manager.h"

using namespace std;
using namespace testing::ext;
using namespace OHOS::NativeRdb;

namespace OHOS {
namespace Media {

static shared_ptr<MediaLibraryRdbStore> g_rdbStore;
static uint64_t g_shellToken = 0;
static MediaLibraryMockHapToken* mockToken = nullptr;

void TestClassNameTest::SetUpTestCase(void)
{
    MediaLibraryUnitTestUtils::Init();
    g_shellToken = IPCSkeleton::GetSelfTokenID();
    MediaLibraryMockTokenUtils::RestoreShellToken(g_shellToken);

    vector<string> perms;
    perms.push_back("ohos.permission.GET_NETWORK_INFO");
    mockToken = new MediaLibraryMockHapToken("com.ohos.medialibrary.medialibrarydata", perms);
    for (auto &perm : perms) {
        MediaLibraryMockTokenUtils::GrantPermissionByTest(IPCSkeleton::GetSelfTokenID(), perm, 0);
    }

    g_rdbStore = MediaLibraryUnistoreManager::GetInstance().GetRdbStore();
    if (g_rdbStore == nullptr) {
        MEDIA_ERR_LOG("Failed to get rdbstore");
        exit(1);
    }
    SetTables();
}

void TestClassNameTest::TearDownTestCase(void)
{
    if (!MediaLibraryUnitTestUtils::IsValid()) {
        MediaLibraryUnitTestUtils::Init();
    }
    CleanTestTables();
    g_rdbStore = nullptr;
    MediaLibraryDataManager::GetInstance()->ClearMediaLibraryMgr();
    this_thread::sleep_for(chrono::seconds(1));

    if (mockToken != nullptr) {
        delete mockToken;
        mockToken = nullptr;
    }

    MediaLibraryMockTokenUtils::ResetToken();
    SetSelfTokenID(g_shellToken);
    std::this_thread::sleep_for(std::chrono::seconds(1));
}

void TestClassNameTest::SetUp()
{
    ASSERT_NE(g_rdbStore, nullptr);
    ClearAndRestart();
}

void TestClassNameTest::TearDown() {}

} // namespace Media
} // namespace OHOS
```

### 2. Service Test Pattern

For testing controller services (MediaAssetsControllerService, MediaAlbumsControllerService):

```cpp
using ServiceCall = std::function<void(MessageParcel &data, MessageParcel &reply)>;

int32_t ServiceCreateAsset(CreateAssetReqBody &reqBody, ServiceCall call)
{
    MessageParcel data;
    if (reqBody.Marshalling(data) != true) {
        MEDIA_ERR_LOG("reqBody.Marshalling failed");
        return -1;
    }

    MessageParcel reply;
    call(data, reply);

    IPC::MediaRespVo<CreateAssetRespBody> respVo;
    if (respVo.Unmarshalling(reply) != true) {
        MEDIA_ERR_LOG("respVo.Unmarshalling failed");
        return -1;
    }

    int32_t errCode = respVo.GetErrCode();
    if (errCode != 0) {
        MEDIA_ERR_LOG("respVo.GetErrCode: %{public}d", errCode);
        return errCode;
    }

    return respVo.GetBody().fileId;
}

HWTEST_F(CreateAssetTest, PublicCreateAsset_Test_001, TestSize.Level0)
{
    MEDIA_INFO_LOG("Start PublicCreateAsset_Test_001");
    int32_t fileId = PublicCreateAsset("xxx");
    ASSERT_LT(fileId, 0);

    fileId = PublicCreateAsset("jpg", "Public_002.xxx");
    ASSERT_LT(fileId, 0);
}
```

### 3. State/Getter-Setter Test Pattern

For testing state management functions:

```cpp
HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataCleanState_test_001, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataCleanState_test_001 Start");
    SetSmartDataCleanState(CleanTaskState::CLEANING);
    int64_t state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::CLEANING));
    MEDIA_INFO_LOG("SmartDataCleanState_test_001 End");
}

HWTEST_F(CloudMediaRetainSmartDataTest, SmartDataCleanState_test_002, TestSize.Level1)
{
    MEDIA_INFO_LOG("SmartDataCleanState_test_002 Start");
    SetSmartDataCleanState(CleanTaskState::IDLE);
    int64_t state = GetSmartDataCleanState();
    EXPECT_EQ(state, static_cast<int64_t>(CleanTaskState::IDLE));
    MEDIA_INFO_LOG("SmartDataCleanState_test_002 End");
}
```

### 4. Database Operation Test Pattern

For testing DAO and database operations:

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

### 5. Boundary Condition Test Pattern

For testing edge cases and invalid inputs:

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

### 6. Integration Test Pattern

For testing multiple components working together:

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

## Assertion Patterns

| Test Type | Assertion Pattern |
|-----------|-------------------|
| Success | `EXPECT_EQ(ret, E_OK)` or `EXPECT_GT(fileId, 0)` |
| Error | `EXPECT_LT(fileId, 0)` or `EXPECT_EQ(ret, E_ERR)` |
| Boolean true | `EXPECT_TRUE(condition)` |
| Boolean false | `EXPECT_FALSE(condition)` |
| Null check | `ASSERT_NE(resultSet, nullptr)` |
| State equality | `EXPECT_EQ(state, expectedValue)` |

## Test Levels

- **TestSize.Level0**: Critical path tests (happy path, basic functionality)
- **TestSize.Level1**: Extended tests (edge cases, boundary conditions, error handling)

## BUILD.gn Template

See [assets/BUILD.gn.template](assets/BUILD.gn.template) for complete build configuration template.

## References

- [Test Patterns](references/test-patterns.md) - Detailed test patterns and examples
- [Common Utilities](references/common-utilities.md) - Test utilities and helper functions
