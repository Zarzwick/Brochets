#ifndef WINDOW_H
#define WINDOW_H

#include <QtWidgets/QMainWindow>
#include <QtGui/QPushButton>
#include <QtGui/QLabel>
#include <QtWidgets/QWidget>
#include <QtCore/QTimer>

class Render;

namespace ui
{
    class Window : public QMainWindow
    {
        Q_OBJECT
        public:
            explicit Window(QWidget *parent = 0);
            ~Window();
            
            virtual void resizeEvent(QResizeEvent *);
        private:
        public slots:
            virtual void button1Event();
            virtual void button2Event();
            virtual void button3Event();
            virtual void button4Event();
        private:
            QPushButton *button[4];
            Render *render;
    };
}

#endif
