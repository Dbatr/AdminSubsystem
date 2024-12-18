package ru.backend.auth.services;

import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import ru.backend.auth.models.UserRole;
import ru.backend.auth.repositories.UserProfileRepository;
import ru.backend.auth.repositories.UserRepository;
import ru.backend.auth.models.User;
import ru.backend.auth.utils.AuthResponse;
import ru.backend.auth.utils.LoginRequest;
import ru.backend.auth.utils.RegisterRequest;
import ru.backend.auth.models.UserProfile;

import java.time.LocalDateTime;


@Service
@RequiredArgsConstructor
public class AuthService {

    private final PasswordEncoder passwordEncoder;
    private final UserRepository userRepository;
    private final JwtService jwtService;
    private final RefreshTokenService refreshTokenService;
    private final AuthenticationManager authenticationManager;

    private final UserProfileRepository userProfileRepository;

    public AuthResponse register(RegisterRequest registerRequest) {
        var user = User.builder()
                .email(registerRequest.getEmail())
                .password(passwordEncoder.encode(registerRequest.getPassword()))
                .role(UserRole.USER)
                .status(true)
                .build();

        User savedUser = userRepository.save(user);

        // Создание пустого профиля для нового пользователя
        UserProfile userProfile = new UserProfile();
        userProfile.setUser(savedUser); // связываем профиль с пользователем

        // Установка значений по умолчанию, если нужно
        // Например: userProfile.setName("Default Name");

        // Сохранение профиля
        userProfile = userProfileRepository.save(userProfile); // Сохраняем профиль и получаем его id

        // Установка userProfileId в User
        savedUser.setUserProfile(userProfile);
        userRepository.save(savedUser);

        var accessToken = jwtService.generateToken(savedUser);
        var refreshToken = refreshTokenService.createRefreshToken(savedUser.getEmail());

        return AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken.getRefreshToken())
                .build();
    }

    public AuthResponse login(LoginRequest loginRequest) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        loginRequest.getEmail(),
                        loginRequest.getPassword()
                )
        );

        var user = userRepository.findByEmail(loginRequest.getEmail()).orElseThrow(() -> new UsernameNotFoundException("User not found!"));

        // Обновляем время последнего входа
        user.setLastLogin(LocalDateTime.now());
        userRepository.save(user);

        var accessToken = jwtService.generateToken(user);
        var refreshToken = refreshTokenService.createRefreshToken(loginRequest.getEmail());

        return AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken.getRefreshToken())
                .build();
    }

    public User getUserByEmail(String email) {
        return userRepository.findByEmail(email)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }
}
