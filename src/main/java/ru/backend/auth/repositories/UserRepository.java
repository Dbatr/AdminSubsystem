package ru.backend.auth.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.auth.models.User;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
