<?php
$connection = ssh2_connect('localhost', 22);
ssh2_auth_password($connection, 'root', '12345678');
$stream = ssh2_exec($connection,'hostname');
stream_set_blocking($stream, true);
while($line = fgets($stream)) {
    echo $line;
}
?>
