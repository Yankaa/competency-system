# Система управления моделью компетенций

Система состоит из нескольких модулей, написанных на языке Python с использованием фреймворка Flask.

### competency_manager
**Модуль управления моделью компетенций.**
Осуществляет хранение и операций над моделью компетенций.

###	labor_manager
**Модуль управления трудовыми ресурсами.**
Осуществляет хранение компетенций трудовых ресурсах.
Предоставляет возможность произведения операций над хранимой информацией, таких как поиск соответствующих друг другу трудовых ресурсов.

###	standard_analyzer
**Модуль формирования модели компетенций из профессиональных стандартов.**
Осуществляет скачивание, анализ и выделение компетенций из профессиональных стандартов.
Добавляет выделенные компетенции в *модуль управления моделью компетенций*.

###	user_start
**Главная страница системы.**
Направляет посетителя системы в нужный модуль.
Позволяет ознакомится со списком наиболее востребованных компетенций.

###	worker
**Модуль соискателя.**
Предоставляет пользователю следующие возможности:
- управление компетенциями, которыми владеет соискатель
- поиск вакансий, которые больше всего подходят соискателю
- поиск компетенций, изучение которых сделает соискателя более востребованным на рынке труда

###	employer
**Модуль работодателя.**
Предоставляет пользователю следующие возможности:
- создание и управление вакансиями
- управление компетенциями, которые необходимы для заданной компетенции
- поиск соискателей, которые лучше всего подходят для заданной компетенции