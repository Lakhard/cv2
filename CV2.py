import cv2

# Захват видео с веб-камеры (0 - индекс камеры по умолчанию)
cap = cv2.VideoCapture(0)

while True:
    # Чтение кадра с камеры
    ret, frame = cap.read()

    if not ret:
        print("Не удалось получить кадр")
        break

    # Конвертация в серый (для упрощения обработки)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Детекция лиц (требуется файл каскада)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Рисование прямоугольников вокруг лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Отображение кадра
    cv2.imshow('Computer Vision', frame)

    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()