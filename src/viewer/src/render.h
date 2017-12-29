#ifndef RENDER_H
#define RENDER_H

#include <QWidget>
#include <QGraphicsView>
#include <QLineEdit>
#include <QMouseEvent>
#include <QDirIterator>
#include <QGraphicsLineItem>
#include "jsonpp.hpp"
#include <list>

struct FileInfo
{
    QString filename;
    QRectF inner;
    QRectF outer;
    QString id;
};

class Render : public QGraphicsView
{
    public:
        Render(QWidget *parent = 0);
        virtual ~Render();
        
        void next();
        void previous();
        void save();
        void load();
        
        virtual void mouseMoveEvent(QMouseEvent*);
        virtual void mousePressEvent(QMouseEvent*);
        virtual void mouseReleaseEvent(QMouseEvent*);

        virtual void wheelEvent(QWheelEvent* event);
        virtual void keyPressEvent(QKeyEvent*);
    private:
        QLineEdit *id;
        QGraphicsScene scene;
        QGraphicsRectItem *inner;
        QGraphicsRectItem *outer;
        QGraphicsPixmapItem *background;
        QPointF start, origin;
    private:
        std::list<FileInfo> files;
        std::list<FileInfo>::iterator current;
        bool move, doinner, doouter;
};

#endif