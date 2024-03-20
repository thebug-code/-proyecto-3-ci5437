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

        return matches

    def cnf_clause(self):
        clauses = []
        matches = self.match_generator()

        print(matches)

        # restricción 1: no se pueden jugar dos partidos al mismo tiempo
        for date in self.dates:
            for hour in self.hours:
                # Se obtienen los partidos que se juegan en la misma fecha y hora
                matches_date_hour = [(local, visitor, date, hour)
                                     for local in self.teams
                                     for visitor in self.teams
                                     if local != visitor]

                # Se crea la cláusula
                for i, partido1 in enumerate(matches_date_hour):
                    for partido2 in matches_date_hour[i+1:]:
                        clause = [-matches[partido1], -matches[partido2]]
                        clauses.append(clause)

        # restricción 2: un equipo no puede jugar dos partidos el mismo día
        for date in self.dates:
            for team in self.teams:
                # Se obtienen los partidos de un equipo en la misma fecha
                matches_date_team = [(local, visitor, date, hour)
                                     for hour in self.hours
                                     for local in self.teams
                                     for visitor in self.teams
                                     if local != visitor and (local == team or visitor == team)]

                if len(matches_date_team) > 1:
                    # Se crea la cláusula
                    for i in range(len(matches_date_team)):
                        for j in range(i+1, len(matches_date_team)):
                            clause = [-matches[matches_date_team[i]
                                               ], -matches[matches_date_team[j]]]
                            clauses.append(clause)

        # restricción 3: un equipo no puede jugar como local dias consecutivos o como visitante dias consecutivos
        for team in self.teams:
            for i in range(len(self.dates)-1):
                actual_date = self.dates[i]
                next_date = self.dates[i+1]

                # Se obtienen los partidos de un equipo en la fecha actual y la siguiente de local
                matches_local = [(team, visitor, actual_date, hour)
                                 for hour in self.hours
                                 for visitor in self.teams
                                 if team != visitor]

                next_matches_local = [(team, visitor, next_date, hour)
                                      for hour in self.hours
                                      for visitor in self.teams
                                      if team != visitor]

                # Se obtienen los partidos de un equipo en la fecha actual y la siguiente de visitante
                matches_visitor = [(local, team, actual_date, hour)
                                   for hour in self.hours
                                   for local in self.teams
                                   if local != team]

                next_matches_visitor = [(local, team, next_date, hour)
                                        for hour in self.hours
                                        for local in self.teams
                                        if local != team]

                # Se crea la cláusula que impide que un equipo juegue dos partidos seguidos de local
                for match_actual in matches_local:
                    for match_next in next_matches_local:
                        clause = [-matches[match_actual], -matches[match_next]]
                        clauses.append(clause)

                # Se crea la cláusula que impide que un equipo juegue dos partidos seguidos de visitante
                for match_actual in matches_visitor:
                    for match_next in next_matches_visitor:
                        clause = [-matches[match_actual], -matches[match_next]]
                        clauses.append(clause)

        return clauses


# prueba
file = 'ejemplo1.json'
data = rj.read_json_file(file)
traductor = TraductorCNF(data)
cnf = traductor.cnf_clause()
print(cnf)
