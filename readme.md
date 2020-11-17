# Great Heart CRM

# PnL dev. team

CRM-система, призванная содержать в порядке всю информацию о подопечных фонда.

Для запуска: ```python app.py```

В рамках CRM реализован процесс ведения подопечных, сотрудников, спонсоров и благотворителей: есть формы регистрации для каждой из этих категории людей, возможность просматривать их список и редактировать данные по мере необходимости.

Проект реализован на веб-фреймворке [Flask](http://flask.pocoo.org/), оторый позволяет оперативное расширение функционала и предоставляет широкие влозможности по масштабированию сервиса.

База данных реализована в рамках концепции [Serverless](https://en.wikipedia.org/wiki/Serverless_computing); на виртуальном сервере развернута [PostgreSQL](https://www.postgresql.org). База не требует доработки, но может быть расширена в соответствии с новыми требованиями заказчика.