package ru.backend.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.backend.dtos.RoleDTO;
import ru.backend.models.Role;
import ru.backend.repositories.RoleRepository;

import java.util.List;
import java.util.Optional;

@Service
public class RoleService {
    private final RoleRepository roleRepository;

    @Autowired
    public RoleService(RoleRepository roleRepository) {
        this.roleRepository = roleRepository;
    }

    // Получение всех ролей
    public List<Role> getAllRoles() {
        return roleRepository.findAll();
    }

    // Получение роли по ID
    public Optional<Role> getRoleById(Integer id) {
        return roleRepository.findById(id);
    }

    // Добавление новой роли
    public Role addRole(RoleDTO roleDTO) {
        Role role = new Role();
        role.setName(roleDTO.getName());
        return roleRepository.save(role);
    }

    // Удаление роли по ID
    public void deleteRole(Integer id) {
        roleRepository.deleteById(id);
    }
}
