package main;

import naturesimulator.NatureSimulator;
import project.Herbivore;
import project.Plant;
import ui.ApplicationWindow;

import java.awt.*;

/**
 * The main class that can be used as a playground to test your project. This
 * class will be discarded and replaced with our own grading class.
 *
 * IMPORTANT: All the classes that you create should be put under the package
 * named "project". All the other packages will be reset when grading your
 * project.
 */
public class Main {

	/**
	 * Main entry point for the application.
	 *
	 * IMPORTANT: You can change anything in this method to test your game, but your
	 * changes will be discarded when grading your project.
	 *
	 * @param args
	 *            application arguments
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(() -> {
			try {
				// Create game
				// You can change the world width and height, size of each grid square in pixels
				// or the game speed
				NatureSimulator game = new NatureSimulator(50, 50, 10, 10);

				// Create and add plants
				for (int i = 0; i < 200; i++) {
					int x = (int) (Math.random() * game.getGridWidth());
					int y = (int) (Math.random() * game.getGridHeight());
					game.addCreature(new Plant(x, y));
				}

				// Create and add herbivores
				for (int i = 0; i < 20; i++) {
					int x = (int) (Math.random() * game.getGridWidth());
					int y = (int) (Math.random() * game.getGridHeight());
					game.addCreature(new Herbivore(x, y));
				}

				// Create application window that contains the game panel
				ApplicationWindow window = new ApplicationWindow(game.getGamePanel());
				window.getFrame().setVisible(true);

				// Start game
				game.start();

			} catch (Exception e) {
				e.printStackTrace();
			}
		});
	}

}
