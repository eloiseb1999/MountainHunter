from code.Background import Background
from code.const import WIN_WIDTH


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:

            case 'Level1Bg':
                list_bg = []

                for i in range(7):
                    list_bg.append(Background(name=f'Level1Bg{i}', position=(0, 0)))
                    list_bg.append(Background(name=f'Level1Bg{i}', position=(WIN_WIDTH, 0)))

                return list_bg