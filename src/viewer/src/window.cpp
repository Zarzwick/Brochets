#include "render.h"
#include "window.h"

#include <QtGui/QApplication>
#include <QtGui/QDesktopWidget>

#define WIDTH   800
#define HEIGHT  600

namespace ui
{
    Window::Window(QWidget *parent, const QString &filename)
        : QMainWindow(parent)
    {
        setMinimumSize(800, 600);
        
        render = new Render(this, filename);
        render->setAlignment(Qt::AlignLeft | Qt::AlignTop);
        //render->setFixedSize(size());
        setCentralWidget(render);
        
        int pos = 40;
        for(unsigned char i = 0; i<4; ++i)
        {
            button[i] = new QPushButton(this);
            button[i]->setGeometry(pos, 5, 85, 25);
            button[i]->setEnabled(true);
            pos += 80;
        }
        
        button[0]->setText("Previous");
        button[1]->setText("Next");
        button[2]->setText("Save");
        button[3]->setText("Load");
        
        QObject::connect(button[0], SIGNAL(clicked()), this, SLOT(button1Event()));
        QObject::connect(button[1], SIGNAL(clicked()), this, SLOT(button2Event()));
        QObject::connect(button[2], SIGNAL(clicked()), this, SLOT(button3Event()));
        QObject::connect(button[3], SIGNAL(clicked()), this, SLOT(button4Event()));
        
        move(
            (QApplication::desktop()->width()-WIDTH)/2,
            (QApplication::desktop()->height()-HEIGHT)/2
        );
    }
    Window::~Window()
    {
        delete render;
    }
    void Window::resizeEvent(QResizeEvent *)
    {
        render->resize(size());
    }
    void Window::button1Event()
    {
        render->previous();
    }
    void Window::button2Event()
    {
        render->next();
    }
    void Window::button3Event()
    {
        render->save();
    }
    void Window::button4Event()
    {
        render->load();
    }
}
