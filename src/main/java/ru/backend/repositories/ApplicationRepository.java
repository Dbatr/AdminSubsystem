package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Application;

@Repository
public interface ApplicationRepository extends JpaRepository<Application, Long> {
}
