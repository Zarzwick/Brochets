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
        using FilesStorage = std::list<FileInfo>;
        using FilesStorageIt = FilesStorage::iterator;
    public:
        Render(QWidget *parent = 0, const QString &filename = "entities.json");
        virtual ~Render();
        
        void next();
        void previous();
        void save();
        void load();
        
        inline FilesStorageIt find(QString filename)
        {
            return std::find_if(
                std::begin(files), std::end(files),
                [&]( const FileInfo &v ){
                    return v.filename == filename;
                }
            );
        }
        
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
        FilesStorage files;
        FilesStorageIt current;
        bool move, doinner, doouter;
        QString filename;
};

#endif