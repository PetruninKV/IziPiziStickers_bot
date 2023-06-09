#!/bin/bash

# Загрузка значения ID_DATA_SRC_INFLIXDB из файла .env
ID_DATA_SRC_INFLIXDB=$(grep -o "ID_DATA_SRC_INFLIXDB=.*" .env | cut -d "=" -f 2)

# Замена значения "YOUR_ID" на ID_DATA_SRC_INFLIXDB
sed -i "s/\"YOUR_ID\"/\"$ID_DATA_SRC_INFLIXDB\"/g" "dashboard.example.json"
echo "Значение \"YOUR_ID\" в файле dashboard.example.json заменено на ID_DATA_SRC_INFLIXDB."

# Переименование файла в dashboard.json
cp "dashboard.example.json" "dashboard.json"
echo "Файл dashboard.example.json переименован в dashboard.json."
