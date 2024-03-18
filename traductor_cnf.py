import read_json as rj


class TraductorCNF:
    def __init__(self, data):
        self.data = data
        self.teams = rj.get_teams(data)
        self.dates = rj.get_dates(data)
        self.hours = rj.get_hours(data)

    def match_generator(self):
        matches = {}
        match_count = 1

        for date in self.dates:
            for hour in self.hours:
                for local in self.teams:
                    for visitor in self.teams:
                        if local != visitor:
                            # Se crea las variables de los partidos
                            matches[(local, visitor, date, hour)] = match_count
                            match_count += 1

        print(matches)
        return matches

    def cnf_clause(self):
        clauses = []
        matches = self.match_generator()

        # restricción 1: no se pueden jugar dos partidos al mismo tiempo
        for date in self.dates:
            for hour in self.hours:
                # Se obtienen los partidos que se juegan en la misma fecha y hora
                matches_date_hour = [(local, visitor, date, hour)
                                     for local in self.teams for visitor in self.teams if local != visitor]

                # Se crea la cláusula
                for i, partido1 in enumerate(matches_date_hour):
                    for partido2 in matches_date_hour[i+1:]:
                        clause = [-matches[partido1], -matches[partido2]]
                        clauses.append(clause)

        return clauses


# prueba
file = 'ejemplo1.json'
data = rj.read_json_file(file)
traductor = TraductorCNF(data)
print(traductor.cnf_clause())
