from flask import  jsonify
from data import db_session
from flask_restful import Resource, reqparse, abort
from data.news import News
from data.users import User
from data.category import Category

def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")

class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        user = session.query(User).filter(User.id == news_id).first()
        for categ in news.categories: 
                category_id = categ.id
        category = session.query(Category).filter(Category.id == category_id).first()
        return jsonify({'news': {"title":news.title, "content":news.content, "user_name":user.name, "is_private":news.is_private, "category":category.name}})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})
        

class NewsListResource(Resource):
    
    
    def get(self):
        session = db_session.create_session()
        news = session.query(News).filter(User.id==1).all()
        all_data = {}
        i = 0
        for item in news:
            i += 1
            user = session.query(User).filter(User.id == item.user_id).first()
            for categ in item.categories: 
                category_id = categ.id
            category = session.query(Category).filter(Category.id == category_id).first()
            data = {i:{"category":category.name, f'title':item.title, f'content':item.content, f'user.name':user.name}}
            print(data)
            all_data.update(data)
        
        response = {'news':[all_data]}
        return jsonify(response)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('content', required=True)
        parser.add_argument('is_private', required=True, type=bool)
        # parser.add_argument('is_published', required=True, type=bool)
        parser.add_argument('user_id', required=True, type=int)

        args = parser.parse_args()
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'], 
            # is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})

    