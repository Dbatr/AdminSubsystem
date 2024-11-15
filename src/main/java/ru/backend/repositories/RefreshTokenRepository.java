package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.models.RefreshToken;

import java.util.Optional;

public interface RefreshTokenRepository extends JpaRepository<RefreshToken, Long> {
    Optional<RefreshToken> findByRefreshToken(String refreshToken);
}
