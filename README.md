# API Help

## Authentication

For clients to authenticate, the token key should be included in the Authorization HTTP header.
The key should be prefixed by the string literal "Token", with whitespace separating the two strings.

```none
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**NOTE:** Use `python manage.py drf_create_token <username>` to generate tokens for existing users.
