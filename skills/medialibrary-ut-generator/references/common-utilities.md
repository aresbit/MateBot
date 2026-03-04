# Media Library Test Common Utilities

## Test Setup Utilities

### MediaLibraryUnitTestUtils

```cpp
#include "medialibrary_unittest_utils.h"

// Initialize test environment
MediaLibraryUnitTestUtils::Init();

// Check if test environment is valid
bool isValid = MediaLibraryUnitTestUtils::IsValid();

// Create test tables
MediaLibraryUnitTestUtils::CreateTestTables(g_rdbStore, createTableSqlLists);

// Clean test tables
MediaLibraryUnitTestUtils::CleanTestTables(g_rdbStore, testTables);
```

### MediaLibraryUnistoreManager

```cpp
#include "medialibrary_unistore_manager.h"

// Get RDB store instance
auto g_rdbStore = MediaLibraryUnistoreManager::GetInstance().GetRdbStore();
```

### MediaLibraryMockTokenUtils

```cpp
#include "medialibrary_mock_tocken.h"

// Save and restore shell token
uint64_t g_shellToken = IPCSkeleton::GetSelfTokenID();
MediaLibraryMockTokenUtils::RestoreShellToken(g_shellToken);

// Grant permission
MediaLibraryMockTokenUtils::GrantPermissionByTest(IPCSkeleton::GetSelfTokenID(), perm, 0);

// Reset token after tests
MediaLibraryMockTokenUtils::ResetToken();
SetSelfTokenID(g_shellToken);
```

## Common Helper Functions

### Database Helpers

```cpp
// Clear table
static int32_t ClearTable(const string &table)
{
    RdbPredicates predicates(table);
    int32_t rows = 0;
    int32_t err = g_rdbStore->Delete(rows, predicates);
    if (err != E_OK) {
        MEDIA_ERR_LOG("Failed to clear table, err: %{public}d", err);
        return E_HAS_DB_ERROR;
    }
    return E_OK;
}

// Quote string for SQL
static std::string Quote(const std::string &str)
{
    return "'" + str + "'";
}
```

### Result Set Helpers

```cpp
#include "result_set_utils.h"

// Get integer value from result set
int32_t albumId = GetInt32Val(PhotoAlbumColumns::ALBUM_ID, resultSet);

// Get string value from result set
string name = MediaLibraryRdbStore::GetString(resultSet, PhotoAlbumColumns::ALBUM_NAME);
int32_t albumType = MediaLibraryRdbStore::GetInt(resultSet, PhotoAlbumColumns::ALBUM_TYPE);
```

## Common Includes

```cpp
// Standard headers
#include <chrono>
#include <thread>
#include <vector>
#include <string>

// Google Test
#include <gtest/gtest.h>

// Media library headers
#include "media_column.h"
#include "media_file_utils.h"
#include "media_log.h"
#include "medialibrary_errno.h"
#include "medialibrary_rdbstore.h"

// Test utilities
#include "medialibrary_unittest_utils.h"
#include "medialibrary_unistore_manager.h"
#include "medialibrary_data_manager.h"
#include "medialibrary_mock_tocken.h"
```

## Common Macros

```cpp
// Logging tag
#define MLOG_TAG "TestClassName"

// Access private members for testing
#define private public
#define protected public
#include "target_header.h"
#undef private
#undef protected
```

## Common Test Variables

```cpp
// Global RDB store
static shared_ptr<MediaLibraryRdbStore> g_rdbStore;

// Token for permission testing
static uint64_t g_shellToken = 0;
static MediaLibraryMockHapToken* mockToken = nullptr;

// Constants
static constexpr int32_t SLEEP_SECONDS = 1;
static constexpr int32_t TEST_ALBUM_ID = 100;
```

## Common Assertion Patterns

```cpp
// Success checks
EXPECT_EQ(ret, E_OK);
EXPECT_GT(fileId, 0);
EXPECT_GE(count, 0);

// Error checks
EXPECT_LT(fileId, 0);
EXPECT_EQ(ret, E_ERR);
EXPECT_EQ(ret, E_INVALID_VALUES);

// Boolean checks
EXPECT_TRUE(condition);
EXPECT_FALSE(condition);

// Null checks
ASSERT_NE(resultSet, nullptr);
ASSERT_NE(ptr, nullptr);

// String checks
EXPECT_EQ(str1, str2);
EXPECT_GT(str.length(), 0);
```

## Test Size Levels

- `TestSize.Level0`: Critical path, basic functionality tests
- `TestSize.Level1`: Extended tests, edge cases, error handling
- `TestSize.Level2`: Stress tests, performance tests

## Common Sleep Durations

```cpp
// Short wait for async operations
std::this_thread::sleep_for(std::chrono::milliseconds(100));
std::this_thread::sleep_for(std::chrono::milliseconds(500));

// Medium wait for database operations
std::this_thread::sleep_for(std::chrono::seconds(1));

// Long wait for complex operations
std::this_thread::sleep_for(std::chrono::seconds(3));
```
