import cv2
import mediapipe as mp

def abrir_camera():
    captura = cv2.VideoCapture(0)
    
    if not captura.isOpened():
        print("Erro ao abrir a câmera")
        return None
    
    return captura

# Inicializa o mediapipe para detecção de postura
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Lista de pares de pontos para desenhar as linhas da silhueta do corpo
CONECCOES_POSTURA = [
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),
    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
    (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
    (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
    (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE)
]

# Função para desenhar a silhueta e os pontos-chave no frame
def desenhar_silhueta_pontos(imagem, pontos):
    altura, largura, _ = imagem.shape

    # Desenha as conexões da silhueta
    for conexao in CONECCOES_POSTURA:
        ponto1 = pontos[conexao[0].value]
        ponto2 = pontos[conexao[1].value]

        x1, y1 = int(ponto1.x * largura), int(ponto1.y * altura)
        x2, y2 = int(ponto2.x * largura), int(ponto2.y * altura)
        cv2.line(imagem, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Azul (BGR)

    # Desenha os pontos-chave
    for ponto in pontos:
        x, y = int(ponto.x * largura), int(ponto.y * altura)
        cv2.circle(imagem, (x, y), 5, (0, 255, 0), -1)  # Verde (BGR)

# Função para processar o vídeo da câmera em tempo real
def processar_camera(captura):
    while True:
        sucesso, quadro = captura.read()
        if not sucesso:
            break

        # Converte o frame para RGB (necessário para o Mediapipe)
        quadro_rgb = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
        resultado = pose.process(quadro_rgb)

        # Se detectar a postura, desenha os pontos e conexões
        if resultado.pose_landmarks:
            desenhar_silhueta_pontos(quadro, resultado.pose_landmarks.landmark)

        # Exibe o vídeo com a detecção da postura
        cv2.imshow('Detecção de Postura', quadro)

        # Pressionar 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    captura.release()
    cv2.destroyAllWindows()

# Inicia o processamento da câmera
if __name__ == "__main__":
    captura = abrir_camera()
    if captura:
        processar_camera(captura)
