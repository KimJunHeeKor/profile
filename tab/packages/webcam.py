import cv2

from deepface import DeepFace

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from pyqt.profile.data.dataclass import WindowSize


class WebCam(QThread):
    """
    webcam 연결 class
    """
    imageUpdate = pyqtSignal(QImage)
    threadActive = True
    capture = None

    def run(self):
        """
        WebCam Thread run
        @params: None
        :return: None
        """
        while self.threadActive:
            if self.capture is None:
                try:
                    self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                except Exception as e:
                    print(f"Critical ERROR : {e}")

            ret, frame = self.capture.read()

            print(DeepFace.analyze(frame, detector_backend="opencv"))
            if ret:
                self._faceDetection(frame)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedImage = cv2.flip(image, 1)
                convert2Qtform = QImage(flippedImage.data,
                                           flippedImage.shape[1],
                                           flippedImage.shape[0],
                                           QImage.Format_RGB888)
                picture = convert2Qtform.scaled(WindowSize.maximum_width, # width
                                                   WindowSize.maximum_height, # height
                                                   Qt.KeepAspectRatio)

                self.imageUpdate.emit(picture)

    def activeRunWebCam(self):
        """
        WebCam running is active
        @params: None
        :return: None
        """
        self.threadActive = True

    def deactiveRunWebCam(self):
        """
        WebCam running is deactive
        @params: None
        :return: None
        """
        self.threadActive = False

    def quitWebCam(self):
        """
        Quit the WebCam running
        @params:None
        :return: None
        """
        self.threadActive = False

        if self.capture is None:
            return

        if self.capture.isOpened():
            self.capture.release()
            self.wait(1500)
            del self.capture

    def _faceDetection(self, Image):
        """
        Detect faces at input image, then draw rectangle at face boundary in the input image
        :param Image: Image
        :return: Image
        """

        face_cascade = cv2.CascadeClassifier("face/haarcascade_frontalface_default.xml")
        # eye_cascade = cv2.CascadeClassifier("face/haarcascade_eye.xml")
        # smile_cascade = cv2.CascadeClassifier("face/haarcascade_smile.xml")

        faces = face_cascade.detectMultiScale(image=Image, scaleFactor=1.3, minNeighbors=5)

        for (x_face, y_face, w_face, h_face) in faces:
            cv2.rectangle(Image, (x_face, y_face), (x_face + w_face, y_face + h_face), (255, 130, 0), 2)
            ## 추후 확인
            # ri_grayscale = grayscale[y_face:y_face + h_face, x_face:x_face + w_face]
            # ri_color = Image[y_face:y_face + h_face, x_face:x_face + w_face]
            # eye = eye_cascade.detectMultiScale(ri_grayscale, 1.2, 18)
            # for (x_eye, y_eye, w_eye, h_eye) in eye:
            #     cv2.rectangle(ri_color, (x_eye, y_eye), (x_eye + w_eye, y_eye + h_eye), (0, 180, 60), 2)
            # smile = smile_cascade.detectMultiScale(ri_grayscale, 1.7, 20)
            # for (x_smile, y_smile, w_smile, h_smile) in smile:
            #     cv2.rectangle(ri_color, (x_smile, y_smile), (x_smile + w_smile, y_smile + h_smile), (255, 0, 130), 2)

        return Image