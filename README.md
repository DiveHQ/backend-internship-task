# Calorie Tracker

REST API for managing and tracking daily calorie intake.

## Assumptions and Choices Made in the Implementation

1. Assumed that an `entry` and `record` refer to the same concept.

2. __Role Identification__

   - Admins in the app are identified using the `is_staff` boolean field provided by Django. This field indicates that the user is an admin.
   - User Managers are identified using a `User Managers` group created and persisted through Django migrations. The purpose of creating a group is to have flexibility in adding different roles in the future without adding a boolean field on the User model for each new role.
   - Regular users are those who do not meet the criteria to be user managers or admins. They are users who are not part of the `User Managers` group and do not have `is_staff` set to true.

3. __Permissions__

   1. Admins:
      - Can perform CRUD operations on all users, entries/records.
   2. User Managers:
      - Can perform CRUD operations only on users and their owned entries/records.
   3. Regular Users:
      - Can perform CRUD operations only on their owned entries/records.
      - Can update only their passwords.
      - Can perform CRUD operations except DELETE on their settings.

4. __User Settings and Default Daily Calories__

   - To implement the `expected daily calories` setting, a separate model/table for user settings was created. This design choice allows for the introduction of other settings in the future.
   - The default value for the `expected daily calories` setting was set to 2250, representing a reasonable average.

5. __Handling Missing Calories from Provider__

   - When a user does not provide the calories for a meal, an error is __not__ thrown if the calories provider is down or cannot be reached. Instead, the `calories` field is saved as null. This approach assumes that users will be unable to save new entries if the provider is inaccessible.
   - During an update to an entry, the `calories` field can still be ignored, and the API will attempt to fetch the calories from the provider.

6. __Entry Creation and Update__

   - Entries are created and updated before setting the `below daily threshold` boolean. This approach accounts for cases where the incoming entry increases or decreases the total daily calories.
   - When the calories provider cannot find any foods with the query entered (resulting in a 404 response), an error is thrown, and the entry is not saved or updated. This behavior is considered validation for the `text` field in Entries, assuming that the user most likely entered an incorrect meal.

7. __Testing with Calories Provider__

   - Tests involving requests to the calories provider are mocked with the expected response code from the provider. This approach is taken to ensure predictable and controlled testing conditions.
   - However, there is one test that actually makes a request to the calories provider. Currently, this test is skipped because it is meant to be run locally, and the CI environment may reach usage limits for the API key.
