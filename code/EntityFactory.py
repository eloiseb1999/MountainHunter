from code.Background import Background


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):

        match entity_name:

            case 'Level1Bg':
                list_bg = []

                bg_names = [
                    'Level1Bg0',
                    'Level1Bg1',
                    'Level1Bg2',
                    'Level1Bg3'
                    'Level1Bg4'
                    'Level1Bg5'
                    'Level1Bg6'
                ]

                for name in bg_names:
                    list_bg.append(
                        Background(
                            name=name,
                            position=position
                        )
                    )

                return list_bg