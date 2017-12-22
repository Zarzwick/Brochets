#include "render.h"

#include <QDebug>
#include <QScrollBar>
#include <iostream>
#include <fstream>

Render::Render(QWidget *parent)
    : QGraphicsView(parent), move(false),
      doinner(false), doouter(false),
      id(new QLineEdit(parent))
{
    QDirIterator folder("./", QDir::Files, QDirIterator::Subdirectories);
    id->setGeometry(5, 30, 85, 25);
    id->setEnabled(true);
    
    //! skip the first one : the root folder itself
    //folder.next();
    
    while(folder.hasNext())
    {
        FileInfo info;
            info.filename = folder.fileInfo().canonicalFilePath();
            info.inner = QRect{0,0,0,0};
            info.outer = QRect{0,0,0,0};
        files.push_back(info);
        folder.next();
    }

    setScene(&scene);
    setBackgroundBrush(QBrush(Qt::white, Qt::SolidPattern));
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOn);
    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOn);
    
    current = files.begin();
    
    QImage image((*current).filename);
    background = new QGraphicsPixmapItem(QPixmap::fromImage(image));
    background->setPos(0,0);
    scene.addItem(background);
    
    scene.setSceneRect(0.0, 0.0, image.width(), image.height());
    
    inner = scene.addRect(0,0, 0, 0);
    inner->setBrush(QBrush(QColor(0, 255, 0, 125)));
    outer = scene.addRect(0,0, 0, 0);
    outer->setBrush(QBrush(QColor(255, 0, 0, 50)));
}

Render::~Render()
{
    setScene(nullptr);
}

void Render::mouseMoveEvent(QMouseEvent *event)
{
    auto rect = doinner ? inner : nullptr;
         rect = doouter ? outer : rect;
         
    if(rect)
    {
        QPointF c = mapToScene(event->pos());
        
        int x1 = start.x();
        int y1 = start.y();
        int x2 = c.x()-start.x();
        int y2 = c.y()-start.y();
        
        if(x2<0)
        {
            x1 = c.x();
            x2 = start.x()-c.x();
        }
        if(y2<0)
        {
            y1 = c.y();
            y2 = start.y()-c.y();
        }
    
        rect->setRect(x1, y1, x2, y2);
    }
    
    if(move)
    {
        QPointF oldp = mapToScene(origin.x(), origin.y());
        QPointF newp = mapToScene(event->pos());
        QPointF translation = oldp - newp;

        translate(translation.x(), translation.y());
        
        horizontalScrollBar()->setValue( horizontalScrollBar()->value() + translation.x() );
        verticalScrollBar()->setValue( verticalScrollBar()->value() + translation.y() );

        origin = QPointF(event->x(), event->y());
    }
}

void Render::next()
{
    if(current != files.end())
    {
        current->id = id->text();
        current++;
        QImage image(current->filename);
        background->setPixmap(QPixmap::fromImage(image));
        inner->setRect(current->inner);
        outer->setRect(current->outer);
        id->setText(current->id);
    }
}

void Render::previous()
{
    if(current != files.begin())
    {
        current->id = id->text();
        current--;
        QImage image(current->filename);
        background->setPixmap(QPixmap::fromImage(image));
        inner->setRect(current->inner);
        outer->setRect(current->outer);
        id->setText(current->id);
    }
}

void Render::save()
{
    QDir dir("../local");
    json::value v;
    json::object o;
    
    for(auto &it : files)
    {
        QString filename = dir.relativeFilePath(it.filename);
        json::object tmp = {
            { "inner", {it.inner.x(), it.inner.y(), it.inner.width(), it.inner.height()} },
            { "outer", {it.outer.x(), it.outer.y(), it.outer.width(), it.outer.height()} },
            { "id", it.id.toLatin1().data() }
        };
        o[filename.toLatin1().data()] = tmp;
    }
    
    std::ofstream file("entities.json");
    json::dump(file, o);
}

void Render::load()
{
    try
    {
        std::ifstream file("entities.json");
        
        file.seekg(0, std::ios::end);
        int length = file.tellg();
        file.seekg(0, std::ios::beg);
        char *buffer = new char[length];
        file.read(buffer, length);
        file.close();
        
        json::parser p(buffer);
        json::value v;
        p.parse(v);
        
        std::cout << v.type_name() << std::endl;
        
        delete [] buffer;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
}

void Render::mousePressEvent(QMouseEvent *event)
{
    if(Qt::RightButton == event->button())
    {
        doinner = true;
        start = mapToScene(event->pos());
    }
        
    if(Qt::LeftButton == event->button())
    {
        doouter = true;
        start = mapToScene(event->pos());
    }

    if (event->button() == Qt::MidButton)
    {
        origin = QPointF(event->x(), event->y());
        move = true;
    }
}

void Render::mouseReleaseEvent(QMouseEvent *event)
{
    if(Qt::RightButton == event->button())
    {
        auto &it = *current;
        current->inner = inner->rect();
        doinner = false;
    }
    
    if(Qt::LeftButton == event->button())
    {
        auto &it = *current;
        current->outer = outer->rect();
        doouter = false;
    }
    
    if(event->button() == Qt::MidButton)
        move = false;
}

void Render::wheelEvent(QWheelEvent* event)
{
    if (event->delta() > 0)
        scale(1.2, 1.2);
    else
        scale(1.0/1.2, 1.0/1.2);
    event->accept();
}

void Render::keyPressEvent(QKeyEvent*)
{
}
