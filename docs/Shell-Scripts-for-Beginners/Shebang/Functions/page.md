# Functions

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Shebang/Functions/page

Learn to use functions in shell scripts for code reusability and improved maintainability, reducing duplication and simplifying updates.

In this article, you'll learn how to use functions in shell scripts to eliminate code duplication and improve maintainability. Previously, a lengthy sequence of commands was used to create and launch a rocket. If you needed to launch additional rockets, you would duplicate the same set of commands for every mission. This non-modular approach can lead to issues when updates are required, as changing one block would necessitate modifications in every duplicated section.

<Callout icon="lightbulb">
  Using functions in your shell scripts promotes code reusability and makes maintenance easier. Instead of repeating code, you encapsulate the functionality and simply call the function with a parameter.
</Callout>

## Example without Functions

A non-modular script with duplicated code might look like this:

```bash theme={null}
mission_name=$1

mkdir $mission_name
rocket-add $mission_name
rocket-start-power $mission_name
rocket-internal-power $mission_name
rocket-start-sequence $mission_name
rocket-start-engine $mission_name
rocket-lift-off $mission_name

rocket_status=$(rocket-status $mission_name)

while [ "$rocket_status" = "launching" ]
do
  sleep 2
  rocket_status=$(rocket-status $mission_name)
done

if [ "$rocket_status" = "failed" ]
then
  rocket-debug $mission_name
  exit 1
fi
