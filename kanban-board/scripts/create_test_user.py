"""Create test user account."""
from app.core.database import SessionLocal
from app.services import user_service


def main():
    db = SessionLocal()

    try:
        # Check if user already exists
        existing = user_service.get_user_by_username(db, 'testuser')
        if existing:
            print('测试账号已存在')
            print(f'用户名: testuser')
            print(f'邮箱: {existing.email}')
        else:
            # Create test user
            user = user_service.create_user(
                db=db,
                email='test@example.com',
                username='testuser',
                password='Test123456',
                full_name='测试用户',
            )
            # Set as verified
            user.is_verified = True
            db.commit()
            print('测试账号创建成功!')
            print(f'用户ID: {user.id}')
            print(f'用户名: testuser')
            print(f'邮箱: test@example.com')
            print(f'密码: Test123456')
    except Exception as e:
        print(f'创建失败: {e}')
    finally:
        db.close()


if __name__ == '__main__':
    main()
