## App Catalonia Counties and Towns | Commands

This app is based on the official data from the Generalitat de Catalunya.

### Load or updating of counties and towns

From the application Docker terminal run the following command:

    python manage.py update_counties_towns

This will load/update the JSON files in the **Fixtures** *(apps/counties_towns)* folder with the county and town data from the official source.

The app comes with the data already imported from the official source, you
might only need to do that if there's been any changes.

### Importing Counties and Towns in the database

From the application Docker terminal run the following command:

    python manage.py import_counties_towns

This will load all the counties and towns into the application's database.
The list is available in the Admin.
