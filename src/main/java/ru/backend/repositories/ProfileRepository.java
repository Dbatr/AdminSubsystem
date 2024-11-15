package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Profile;

@Repository
public interface ProfileRepository extends JpaRepository<Profile, Long> {

}
