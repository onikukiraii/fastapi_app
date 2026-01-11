from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from entity.user import User
from opensearch.client import index_user, search_users
from params.user import UserCreateParams
from response.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).all()


@router.post("/", response_model=UserResponse)
def create_user(params: UserCreateParams, db: Session = Depends(get_db)) -> User:
    user = User(name=params.name, email=params.email)
    db.add(user)
    db.commit()
    db.refresh(user)

    # OpenSearchにもインデックス
    index_user(
        user_id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at.isoformat(),
    )

    return user


@router.get("/search/")
def search_users_endpoint(q: str) -> list[dict]:
    """
    全文検索でユーザーを検索します。
    OpenSearchを使用して、名前に対してファジーマッチ検索を実行します。
    """
    return search_users(q)
