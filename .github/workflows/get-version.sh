INPUT=$(grep PREFIX_SOFTWARE_VERSION index.php)
SUBSTRING=$(echo $INPUT| cut -d "'" -f 4 )
echo v$SUBSTRING
