# Included features

## `anonymous_required` view decorator

It could be problematic and confusing to allow users to access views like Login,
password restoration or signup while already logged in.

## `absolute_url` helper

This boilerplate is not including the Django's Sites framework setup, assuming
that the project is going to be for a single site.

The current URL can be obtained in the request data, but in situations where
you don't have a request or you cannot rely on it, we need this URL manually
specified somewhere.

This decorator needs you to declare the `ABSOLUTE_URL` setting.

## `BaseModel`

When an authenticated user interacts with the database, you often want to log
their information to keep track of when and who created which registry.

Extend this abstract model when creating models that share this need.

## `PublicMediaStorage` and `PrivateMediaStorage`

### Removal
If your project is not going to store media (or *dynamic*) files, or if you are
not going to use an S3-compatible service to store them, you can remove:

- `base/storage_backends.py`
- The package `storages`
- The package `boto3` (in case you are not going to use other AWSs)

### Usage
In models, specify the storage method like this:

```python
file_field = models.FileField(
    verbose_name="file name",
    storage=PrivateMediaStorage(),
)
```

It's recommended that by default you always use the private storage method.

## `ModelAdminMixin` and `base.ModelAdmin`

If your project doesn't use the admin panel, you can delete it.

Use `ModelAdmin` or the mixin in combination with `BaseModel` to automatically
fill the `created_by` field when saving new registries.
It also adds this functionality to inlines: if you include any inlines in this
admin that has the `created_by` field, it's going to be filled in the inline's
new registries as well.

## Tox and testing
Tox is a command line driven CI frontend and development task automation tool.

At its core tox provides a convenient way to run arbitrary commands in isolated environments to serve as a single entry point for build, test and release activities.

### Usage
To run its tests, you can execute
```
$ tox -e format
$ tox
```
These two commands will try to automatically format your code according to some style guides, and if unable to do so, will present you with the location and reason of the errors.

### Test automatization
To ensure that these tests run before pushing to the remote repository, you can use git *hooks*. Simply place the next script in the **.git/hooks/pre-push** file.
```shell
#!/bin/sh
eval "tox -e format"
eval "tox"
```
This way, git will automatically run the tests for you everytime you try to push to the remote repository, and will abort the push in case it returns an error code, so you can correct it and push again.

# Troubleshooting

## `setuptools` error

When running `poetry install`, if you get this error:

`Can not execute setup.py since setuptools is not available in the build environment.`

Try: `pip install -U setuptools`
In my case, I had `setuptools` v. 60 and got updated to 62.

If it doesn't work for you and you find another solution please add it to this
documentation.

# Deprecations

## MailQueueHandler

In previous versions the boilerplate included this package.
Now the `mailing_manager` cannot be used anymore because of its dependency
of the `mailqueue` package, which is discontinued.
