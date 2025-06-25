# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Login view now redirects users based on role (`is_superuser`, `is_staff`, or default).
- Admin and farmer dashboards with separate templates and views.
- Role-based access control using decorators (`@user_passes_test`, `@login_required`).

### Changed
- Unified login form for both admin and farmer users.

### Fixed
- Error message shown on invalid login or registration attempt.

---

## [1.0.0] - 2025-06-03

### Added
- Initial login and registration views.
- Basic user authentication setup.
