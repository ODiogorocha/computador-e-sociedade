import cv2
import numpy as np

# Caminhos dos arquivos do modelo
model_path = "/home/diogo/Documents/Aulas/Primeiro semestre 2025/computador-e-sociedade-/src/MobileNetSSD_deploy.caffemodel" #caminho real no meu pc
config_path = "/home/diogo/Documents/Aulas/Primeiro semestre 2025/computador-e-sociedade-/src/MobileNetSSD_deploy.prototxt"

# Carrega a rede neural
net = cv2.dnn.readNetFromCaffe(config_path, model_path)

# Lista de classes reconhecidas
classes = [
    "fundo", "avião", "bicicleta", "pássaro", "barco",
    "garrafa", "ônibus", "carro", "gato", "cadeira",
    "vaca", "mesa de jantar", "cachorro", "cavalo", "moto",
    "pessoa", "vaso de planta", "ovelha", "sofá", "trem", "televisor"
]


# Inicia a captura da webcam (0 = câmera padrão)
cap = cv2.VideoCapture(0)

#verifica se a camera foi aberta
if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o frame.")
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    # Varre todas as detecções
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = classes[idx]

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Desenha a caixa e o texto
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            cv2.putText(frame, text, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Mostra o resultado ao vivo
    cv2.imshow("Deteccao em tempo real", frame)

    # Sai do loop ao pressionar a tecla 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

# Libera a câmera e fecha janelas
cap.release()
cv2.destroyAllWindows()
