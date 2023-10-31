from enum import Enum
from typing import Dict

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {"message": "Hello, It is Doggy service!"}


@app.post('/post')
def get_post(time: Timestamp):
    new_timestamp = Timestamp(id=time.id,
                              timestamp=time.timestamp)
    post_db.append(new_timestamp)
    return new_timestamp


@app.get('/dog')
def get_dogs(kind: DogType):
    ls_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
    return ls_dogs



@app.post('/dog')
def create_dog(dog: Dog):
    new_dog = Dog(name=dog.name,
                  pk=dog.pk,
                  kind=dog.kind)
    dogs_db.update({new_dog.pk: new_dog})

    return {'message': 'Dog posted successfully'}


@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int):
    dog = dogs_db.get(pk)
    if dog is not None:
        return dog
    else:
        return {'Error': 'Dog not found'}


@app.patch('/dog/{pk}', response_model=Dog)
def update_dog(pk: int, dog: Dog):
    updated_dog = Dog(name=dog.name,
                  pk=dog.pk,
                  kind=dog.kind)
    dogs_db.update({updated_dog.pk: updated_dog})
    return updated_dog
