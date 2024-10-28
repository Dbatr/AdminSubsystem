package ru.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.logging.Logger;

@SpringBootApplication
public class BackendApplication {

	private static final Logger log = Logger.getLogger(BackendApplication.class.getName());

	public static void main(String[] args) {
		SpringApplication.run(BackendApplication.class, args);
		log.info("Application started in http://localhost:8000");
	}

}
