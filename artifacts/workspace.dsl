workspace "<ЗАПОВНІТЬ назва системи>" "<ЗАПОВНІТЬ короткий опис>" {

    model {
        // Мінімум: 1 person, 2 softwareSystem (одна з тегом "Зовнішня"), 3 container, 6 зв'язків.
        // Синтаксис: id = person "Назва" "Опис"
        //            id = softwareSystem "Назва" "Опис" ["Теги"]
        //            id = container "Назва" "Опис" "Технологія" ["Теги"]
        //            джерело -> ціль "Опис зв'язку" ["Технологія"]
        user = person "<ЗАПОВНІТЬ>" "<ЗАПОВНІТЬ>"

        main = softwareSystem "<ЗАПОВНІТЬ>" "<ЗАПОВНІТЬ>" {
            web = container "<ЗАПОВНІТЬ>" "<ЗАПОВНІТЬ>" "<ЗАПОВНІТЬ>"
        }

        user -> web "<ЗАПОВНІТЬ>" "HTTPS"
    }

    views {
        systemContext main "Context" {
            include *
            autolayout lr
        }

        container main "Containers" {
            include *
            autolayout lr
        }
    }
}
