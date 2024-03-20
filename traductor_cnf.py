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

    # restrictión 1: no se pueden jugar dos partidos al mismo tiempo
    def one_match(self, matches, clauses):
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

        return clauses

    # restricción 2: un equipo no puede jugar dos partidos el mismo día
    def one_team_one_day(self, matches, clauses):
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

        return clauses

    # restricción 3: un equipo no puede jugar como local dias consecutivos o como visitante dias consecutivos
    def one_team_consecutive_days(self, matches, clauses):
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

    # restricción 4: un equipo juega exactamente una vez como local y una vez como visitante con cada equipo
    def one_team_one_opponent(self, matches, clauses):
        for i in range(len(self.teams)):
            for j in range(i+1, len(self.teams)):
                team = self.teams[i]
                opponent = self.teams[j]

                # Se obtienen los partidos del team contra el opponent como local
                matches_local = [matches[(team, opponent, date, hour)]
                                 for date in self.dates
                                 for hour in self.hours]

                # Se obtienen los partidos del team contra el opponent como visitante
                matches_visitor = [matches[(opponent, team, date, hour)]
                                   for date in self.dates
                                   for hour in self.hours]

                # Se crea la cláusula que impide que el team juegue más de una vez como local contra el opponent
                clauses += self.only_one(matches_local)

                # Se crea la cláusula que impide que el team juegue más de una vez como visitante contra el opponent
                clauses += self.only_one(matches_visitor)

        return clauses

    def only_one(self, match_number):
        clauses = []

        # Al menos un partido ocurre
        clauses.append([match for match in match_number])

        # A lo sumo un partido ocurre
        for i in range(len(match_number)):
            for j in range(i+1, len(match_number)):
                clauses.append([-match_number[i], -match_number[j]])

        return clauses

    def cnf_clause(self):
        clauses = []
        matches = self.match_generator()

        # restricción 1: no se pueden jugar dos partidos al mismo tiempo
        clauses = self.one_match(matches, clauses)

        # restricción 2: un equipo no puede jugar dos partidos el mismo día
        clauses = self.one_team_one_day(matches, clauses)

        # restricción 3: un equipo no puede jugar como local dias consecutivos o como visitante dias consecutivos
        clauses = self.one_team_consecutive_days(matches, clauses)

        # restricción 4: un equipo juega exactamente una vez como local y una vez como visitante con cada equipo
        clauses = self.one_team_one_opponent(matches, clauses)

        return clauses


# prueba
file = 'ejemplo1.json'
data = rj.read_json_file(file)
traductor = TraductorCNF(data)
matches = traductor.match_generator()
print(matches)
cnf = traductor.one_team_one_opponent(matches, [])
print(cnf)
