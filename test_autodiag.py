import unittest

from autodiag import diagnostiquer, evaluer_temperature_moteur


class TestDiagnosticDTC(unittest.TestCase):
    def test_dtc_connu(self):
        resultat = diagnostiquer(" p0300 ")
        self.assertEqual(resultat["code"], "P0300")
        self.assertEqual(resultat["gravite"], "ROUGE")

    def test_dtc_inconnu(self):
        resultat = diagnostiquer("P9999")
        self.assertEqual(resultat["gravite"], "INCONNU")


class TestTemperature(unittest.TestCase):
    def test_temperature_normale(self):
        resultat = evaluer_temperature_moteur(90)
        self.assertEqual(resultat["gravite"], "VERT")

    def test_temperature_en_derives(self):
        resultat = evaluer_temperature_moteur(100)
        self.assertEqual(resultat["gravite"], "ORANGE")

    def test_temperature_elevee(self):
        resultat = evaluer_temperature_moteur(110)
        self.assertEqual(resultat["gravite"], "ROUGE")

    def test_temperature_hors_plage(self):
        with self.assertRaises(ValueError):
            evaluer_temperature_moteur(250)

    def test_temperature_basse_hors_plage(self):
        with self.assertRaises(ValueError):
            evaluer_temperature_moteur(-51)

    def test_temperature_limite_basse_valide(self):
        resultat = evaluer_temperature_moteur(-50)
        self.assertEqual(resultat["gravite"], "VERT")

    def test_temperature_limite_haute_valide(self):
        resultat = evaluer_temperature_moteur(200)
        self.assertEqual(resultat["gravite"], "ROUGE")

    def test_temperature_non_numerique(self):
        with self.assertRaises(ValueError):
            evaluer_temperature_moteur("100")

    def test_temperature_exactement_95(self):
        resultat = evaluer_temperature_moteur(95)
        self.assertEqual(resultat["gravite"], "ORANGE")

    def test_temperature_exactement_105(self):
        resultat = evaluer_temperature_moteur(105)
        self.assertEqual(resultat["gravite"], "ROUGE")


if __name__ == "__main__":
    unittest.main()
