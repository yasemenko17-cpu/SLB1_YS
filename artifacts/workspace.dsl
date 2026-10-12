workspace "Система коледжу" {
    model {
        user = person "Студент" "Користувач системи журналу"
        ext_sms = softwareSystem "SMS Шлюз" "Зовнішній сервіс сповіщень"
        college_sys = softwareSystem "Система коледжу" "Основна платформа журналу" {
            web = container "Веб-додаток" "Інтерфейс користувача" "React"
            api = container "API Сервіс" "Бізнес-логіка" "Python/FastAPI"
            db = container "Сховище даних" "Зберігання інформації" "PostgreSQL"
        }
        
        user -> college_sys "Користується" "HTTPS"
        college_sys -> ext_sms "Надсилає SMS" "REST API"
        user -> web "Користується" "HTTPS"
        web -> api "Викликає" "JSON/HTTPS"
        api -> db "Читає/записує" "SQL"
        api -> ext_sms "Надсилає SMS" "REST API"
    }
    views {
        systemContext college_sys "Context" {
            include *
            autoLayout
        }
        container college_sys "Containers" {
            include *
            autoLayout
        }
    }
}