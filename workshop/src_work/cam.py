import cv2 
def abrir_camera():
    captura = cv2.VideoCapture(0)

    if not captura.isOpened():
        print("Erro ao abrir a camera")
        return
    
    while True:
        ret, frame = captura.read()
        if not ret:
            print("Erro na captura do quadro")
            break

        cv2.imshow('CAMERA', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    captura.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    abrir_camera()