package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.models.crm.Role;

public interface RoleRepository extends JpaRepository<Role, Long> {
}
