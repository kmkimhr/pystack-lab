# pystack-lab 커리큘럼

FastAPI 기반 Python 백엔드 스택을 단계별로 직접 구현하며 학습한다.
오디오 분석/워터마크 등 도메인 특화 로직은 제외하고, 서비스 인프라 레이어 전체를 커버한다.

## 기술 스택

| 분류 | 기술 |
|------|------|
| 웹 프레임워크 | FastAPI + uvicorn |
| 인증 | JWT + Refresh Token, bcrypt, python-jose |
| 캐시 / 브로커 | Redis |
| ORM | SQLAlchemy (async) |
| 마이그레이션 | Alembic |
| 메인 DB | PostgreSQL |
| 비동기 작업 큐 | Celery |
| 파일 스토리지 | MinIO (로컬), AWS S3 (운영) |
| AWS SDK | boto3 |
| 설정 관리 | pydantic-settings |
| 비동기 HTTP 클라이언트 | httpx |
| 패키지 매니저 | uv |
| 린터 / 포매터 | Ruff |
| 테스트 | pytest + pytest-asyncio + testcontainers |
| 컨테이너 | Docker Compose |
| 클라우드 인프라 | AWS ECS, ECR, S3, RDS, ElastiCache |
| IaC | Terraform + VPC |

---

## 단원 구성

```
Unit 0 (환경)
  └─ Unit 1 (FastAPI)
       └─ Unit 2 (DB)
            └─ Unit 3 (인증)
                 └─ Unit 4 (Redis)
                      └─ Unit 5 (Celery)
                           └─ Unit 6 (MinIO)
                                └─ Unit 7 (테스트)
                                     └─ Unit 8 (AWS)
```

---

## Unit 0 — 개발 환경 세팅

**목표:** 프로젝트 뼈대 구성

- [ ] `uv`로 프로젝트 초기화, 가상환경 관리
- [ ] `Ruff` 설정 (린터 + 포매터)
- [ ] `.env` 파일 구조 설계
- [ ] `pydantic-settings`로 설정 클래스 작성
- [ ] `Docker Compose` 기본 파일 작성 (이후 서비스들 추가해가는 베이스)

---

## Unit 1 — FastAPI 기초

**목표:** API 서버 띄우고 라우터 구조 잡기

- [ ] `FastAPI` + `uvicorn` 실행
- [ ] 라우터 분리 (`APIRouter`, prefix, tags)
- [ ] Request / Response 스키마 (`Pydantic` 모델)
- [ ] 의존성 주입 (`Depends`) 패턴 이해
- [ ] 전역 예외 핸들러, 미들웨어 기초

---

## Unit 2 — 데이터베이스 (PostgreSQL + SQLAlchemy async + Alembic)

**목표:** 비동기 DB 연결과 마이그레이션 파이프라인 구축

- [ ] `Docker Compose`에 PostgreSQL 추가
- [ ] `SQLAlchemy` async 엔진 / 세션 설정
- [ ] 모델 정의 (`DeclarativeBase`)
- [ ] `Alembic` 초기화, `env.py` async 설정
- [ ] 마이그레이션 생성 → 적용 → 롤백 사이클 실습
- [ ] Repository 패턴으로 DB 접근 레이어 분리

---

## Unit 3 — 인증 (JWT + Refresh Token)

**목표:** 회원가입 / 로그인 / 토큰 갱신 플로우 완성

- [ ] `bcrypt`로 비밀번호 해싱
- [ ] `python-jose`로 Access Token 발급
- [ ] Refresh Token 발급 및 DB 저장
- [ ] `Depends`로 현재 유저 추출하는 미들웨어
- [ ] Access Token 만료 → Refresh Token으로 재발급 플로우
- [ ] 로그아웃 (Refresh Token 무효화)

---

## Unit 4 — Redis (캐시)

**목표:** Redis를 캐시 레이어로 활용

- [ ] `Docker Compose`에 Redis 추가
- [ ] `redis-py` async 클라이언트 연결
- [ ] Refresh Token을 Redis에 저장 (Unit 3 개선)
- [ ] API 응답 캐싱 패턴 실습
- [ ] TTL, 키 네이밍 전략

---

## Unit 5 — Celery (비동기 작업 큐)

**목표:** 무거운 작업을 백그라운드로 분리

- [ ] `Docker Compose`에 Celery worker 추가 (브로커: Redis)
- [ ] Task 정의, `delay()` / `apply_async()` 호출
- [ ] Task 상태 추적 (Celery result backend)
- [ ] FastAPI 엔드포인트에서 Task 실행 → Task ID 반환 → 상태 조회 패턴
- [ ] 재시도 전략 (`retry`, `max_retries`)

---

## Unit 6 — 파일 스토리지 (MinIO + boto3)

**목표:** S3 호환 스토리지로 파일 업로드 / 다운로드

- [ ] `Docker Compose`에 MinIO 추가
- [ ] `boto3`로 MinIO 연결 (endpoint_url로 로컬 가리키기)
- [ ] Presigned URL 발급 (업로드용 / 다운로드용)
- [ ] 파일 메타데이터 DB 저장 패턴
- [ ] 운영 환경에서는 같은 코드로 AWS S3 전환되는 구조 이해

---

## Unit 7 — 테스트

**목표:** 신뢰할 수 있는 테스트 스위트 구성

- [ ] `pytest` + `pytest-asyncio` 기본 설정
- [ ] `testcontainers`로 테스트용 실제 PostgreSQL / Redis 컨테이너 실행
- [ ] DB 픽스처, 트랜잭션 롤백 전략
- [ ] `httpx.AsyncClient`로 FastAPI 엔드포인트 통합 테스트
- [ ] 인증이 필요한 엔드포인트 테스트 (토큰 픽스처)
- [ ] Celery Task 테스트 (`CELERY_TASK_ALWAYS_EAGER`)

---

## Unit 8 — AWS 인프라 (Terraform)

**목표:** 로컬 Docker Compose → AWS 클라우드로 이전

- [ ] Terraform 기초 (provider, resource, variable, output)
- [ ] VPC, 서브넷, 보안그룹 구성
- [ ] AWS RDS (PostgreSQL) 프로비저닝
- [ ] AWS ElastiCache (Redis) 프로비저닝
- [ ] AWS S3 버킷 생성 (MinIO → S3 전환 확인)
- [ ] AWS ECR에 도커 이미지 Push
- [ ] AWS ECS (Fargate) 서비스 배포
- [ ] 환경변수를 AWS Secrets Manager / Parameter Store로 관리
