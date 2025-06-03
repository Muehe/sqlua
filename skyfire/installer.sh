#!/bin/bash

clear
echo -e "\033[0;31m"
echo "          ┌───────────────────────────────┐"
echo "          │                               │"
echo "          │    Welcome to the world DB    │"
echo "          │              for              │"
echo "          │        SkyFireEMU  5.4.8      │"
echo "          │        Installation Tool      │"
echo "          │                               │"
echo "          └───────────────────────────────┘"
echo -e "\033[0m"
echo
echo "Please enter your MySQL Info..."
read -p "MySQL Server Address (e.g. localhost): " host
read -p "MySQL Username: " user
read -sp "MySQL Password: " pass
echo
read -p "World Database: " world_db
charset="utf8"
read -p "MySQL Port: " port
dumppath="./dump/"
devsql="./main_db/world/"
procsql="./main_db/procs/"
changsql="./world_updates"

while true; do
    clear
    echo
    echo "    1 - Install 5.4.8 World Database and all updates, NOTE! Whole db will be overwritten!"
    echo
    echo "    W - Backup World Database."
    echo "    C - Backup Character Database."
    echo "    U - Import Changeset."
    echo
    echo "    S - Change your settings"
    echo
    echo "    X - Exit this tool"
    echo
    read -p "Enter a char: " v

    case $v in
        1)
            clear
            echo "First, let's create the database (or overwrite old)!"
            echo "DROP DATABASE IF EXISTS \`$world_db\`;" > "$devsql/databaseclean.sql"
            echo "CREATE DATABASE IF NOT EXISTS \`$world_db\`;" >> "$devsql/databaseclean.sql"
            mysql --host="$host" --user="$user" --password="$pass" --port="$port" --default-character-set="$charset" < "$devsql/databaseclean.sql"
            rm "$devsql/databaseclean.sql"

            echo "Let's make a clean database."
            echo "Adding Stored Procedures"
            for file in "$procsql"/*.sql; do
                echo "Importing: $(basename "$file")"
                mysql --host="$host" --user="$user" --password="$pass" --port="$port" --default-character-set="$charset" "$world_db" < "$file"
            done
            echo "Stored Procedures imported successfully!"

            echo "Installing World Data"
            echo "Importing Data now..."
            for file in "$devsql"/*.sql; do
                echo "Importing: $(basename "$file")"
                mysql --host="$host" --user="$user" --password="$pass" --port="$port" --default-character-set="$charset" "$world_db" < "$file"
                echo "Successfully imported $(basename "$file")"
            done

            echo "Importing Changesets"
            for file in "$changsql"/*.sql; do
                echo "Importing: $(basename "$file")"
                mysql --host="$host" --user="$user" --password="$pass" --port="$port" --default-character-set="$charset" "$world_db" < "$file"
            done
            echo "Changesets imported successfully!"
            echo "Your current 5.4.8 database is complete."
            echo "Please check the SkyFire repository for any world updates \"/sql/updates\"."
            read -p "Press any key to continue..." ;;
        [Ww])
            clear
            read -p "Enter name of your world DB: " worlddb
            sqlname="world-$(date +%a-%m-%d-%Y--%H-%M)"
            mkdir -p "$dumppath"
            echo "Dumping $sqlname.sql to $dumppath"
            mysqldump --port="$port" -u"$user" -p"$pass" --routines --skip-comments --default-character-set="$charset" --result-file="$dumppath/$sqlname.sql" "$worlddb"
            echo "Done."
            read -p "Press any key to continue..." ;;
        [Cc])
            clear
            read -p "Enter name of your character DB: " chardb
            sqlname="char-$(date +%a-%m-%d-%Y--%H-%M)"
            mkdir -p "$dumppath"
            echo "Dumping $sqlname.sql to $dumppath"
            mysqldump -u"$user" -p"$pass" --routines --skip-comments --default-character-set="$charset" --result-file="$dumppath/$sqlname.sql" "$chardb"
            echo "Done."
            read -p "Press any key to continue..." ;;
        [Uu])
            clear
            echo "Importing Changesets"
            for file in "$changsql"/*.sql; do
                echo "Importing: $(basename "$file")"
                mysql --host="$host" --user="$user" --password="$pass" --port="$port" --default-character-set="$charset" "$world_db" < "$file"
            done
            echo "Changesets imported successfully!"
            read -p "Press any key to continue..." ;;
        [Ss])
            exec "$0" ;;
        [Xx])
            exit 0 ;;
        *)
            echo "Please enter a correct character."
            read -p "Press any key to continue..." ;;
    esac
done