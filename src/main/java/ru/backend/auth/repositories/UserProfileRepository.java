package ru.backend.auth.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.auth.models.UserProfile;

public interface UserProfileRepository extends JpaRepository<UserProfile, Long> {
}
